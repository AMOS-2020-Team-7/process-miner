"""
Module used for retrieving log entries and storing them for later analysis.
"""
import csv
import logging
import os
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import List, Dict, Tuple

import process_miner.log_handling.graylog_access as ga
from process_miner.log_handling.graylog_access import GraylogAccess
from process_miner.log_handling.log_filter import LogFilter
from process_miner.log_handling.log_tagger import LogTagger

log = logging.getLogger(__name__)

TIMESTAMP_FILENAME = 'last_included_timestamp'
EXPORTED_FIELDS = ['correlationId', 'timestamp', 'message']


def _get_advanced_timestamp(timestamp: datetime) -> datetime:
    return timestamp + timedelta(milliseconds=1)


def _read_timestamp(path: Path) -> str:
    with path.open('r') as file:
        return file.readline()


def _write_timestamp(timestamp: str, path: Path) -> None:
    with path.open("w") as timestamp_file:
        timestamp_file.write(timestamp)


def _sanitize_filename(filename: str) -> str:
    #  Windows does not support ':' as part of filenames as it is a
    #  reserved character. There are more invalid characters but for now
    #  this should do.
    return filename.replace(':', '_')


class LogRetriever:
    """
    Class used for retrieving and storing log entries.
    """
    def __init__(self, graylog: GraylogAccess, target_dir: str,
                 filter_expressions: List[str], log_taggers: List[LogTagger]):
        self.graylog_access = graylog
        self.log_filter = LogFilter(EXPORTED_FIELDS, 'message',
                                    filter_expressions)
        self.target_dir = Path(target_dir)
        self.log_taggers = log_taggers
        self._folder_lock = Lock()

    def __str__(self) -> str:
        return f'{self.__class__.__name__} [' \
               f'graylog_access <{self.graylog_access}>, ' \
               f'log_filter <{self.log_filter}>, ' \
               f'target_dir <{self.target_dir}>, ' \
               f'log_taggers <{self.log_taggers}>, ' \
               f'_folder_lock <{self._folder_lock}>]'

    def retrieve_logs(self, force: bool = False) -> None:
        """
        Retrieves logs from the configured Graylog instance. Logs are stored
        in the configured directory grouped by their correlationID in separate
        CSV files.
        :param force: force download of already saved logs
        """
        with self._folder_lock:
            self._prepare_target_dir()
            if force:
                self._clear_logs()

            last_retrieved_timestamp = self._load_last_included_timestamp()
            first_timestamp = _get_advanced_timestamp(last_retrieved_timestamp)
            lines = self.graylog_access.get_log_entries(
                first_timestamp, EXPORTED_FIELDS)

            if not lines:
                log.info("no (new) log entries found")
                return

            fields, sorted_lines = self._convert_log_lines_to_dict(lines)
            # filter log entries before they get processed any further
            self.log_filter.filter_log_entries(sorted_lines)
            if not sorted_lines:
                log.info('no new entries after filtering')
                return

            # organize/collect related log entries
            grouped_lines, last_timestamp = self._process_csv_lines(
                sorted_lines
            )

            # add fields based on log tag configuration
            for tagger in self.log_taggers:
                for entries in grouped_lines.values():
                    tagger.tag_entries(entries)
                # make sure each taggers field is later written to the CSV
                # files
                fields.append(tagger.target_field)

            self._store_logs_as_csv(grouped_lines, fields)
            self._store_last_included_timestamp(last_timestamp)

    def _prepare_target_dir(self) -> None:
        log.info('preparing target directory "%s"', self.target_dir)
        if not self.target_dir.exists():
            log.info('creating missing target directory (and parents)...')
            self.target_dir.mkdir(parents=True, exist_ok=True)

    def _clear_logs(self):
        log.info('clearing log directory')
        for file in os.listdir(self.target_dir):
            os.remove(self.target_dir / file)

    def _load_last_included_timestamp(self) -> datetime:
        timestamp_path = self.target_dir.joinpath(TIMESTAMP_FILENAME)
        if timestamp_path.exists() and timestamp_path.is_file():
            log.info('reading last included timestamp from file "%s"',
                     timestamp_path)
            timestamp = _read_timestamp(timestamp_path)
            if ga.timestamp_format_is_valid(timestamp):
                log.info('timestamp of last retrieved log entry: "%s"',
                         timestamp)
                return ga.get_datetime_from_timestamp(timestamp)
            log.error('invalid timestamp format "%s"...', timestamp)
        else:
            log.info("information about last included timestamp not found in "
                     "target directory...")

        default_time = datetime.fromtimestamp(0)
        log.info("...using default timestamp '%s'", default_time)
        return default_time

    def _store_last_included_timestamp(self, timestamp) -> None:
        timestamp_path = self.target_dir.joinpath(TIMESTAMP_FILENAME)
        log.info("storing timestamp of last log entry to file '%s'",
                 timestamp_path)
        _write_timestamp(timestamp, timestamp_path)

    @staticmethod
    def _convert_log_lines_to_dict(lines: List[str]) \
            -> Tuple[List[str], List[Dict[str, str]]]:
        reader = csv.DictReader(lines)
        sorted_list = sorted(reader, key=lambda row: row['timestamp'],
                             reverse=False)
        return list(reader.fieldnames), sorted_list

    @staticmethod
    def _process_csv_lines(entries: List[Dict[str, str]]) -> Tuple[
            Dict[str, List[Dict[str, str]]], str]:
        grouped_lines = LogRetriever._group_by_correlation_id(entries)
        timestamp_of_last_entry = entries[-1]['timestamp']
        return grouped_lines, timestamp_of_last_entry

    @staticmethod
    def _group_by_correlation_id(
            lines: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        grouped_lines = defaultdict(list)
        for line in lines:
            correlation_id = line['correlationId']
            if not correlation_id:
                log.info("omitting row with missing correlationId %s", line)
                continue
            grouped_lines[correlation_id].append(line)
        return grouped_lines

    def _store_logs_as_csv(self, grouped_dict,
                           fieldnames: List[str]) -> None:
        for (correlation_id, log_entries) in grouped_dict.items():
            first_timestamp = log_entries[0]['timestamp']
            filename = f"{first_timestamp}_{correlation_id}.csv"
            file_path = self.target_dir.joinpath(_sanitize_filename(filename))
            log.info("storing process with correlation_id '%s' in file '%s'",
                     correlation_id, file_path)

            # move message to rightmost column
            fieldnames.remove('message')
            fieldnames.append('message')
            with file_path.open("w", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames)
                writer.writeheader()
                writer.writerows(log_entries)
