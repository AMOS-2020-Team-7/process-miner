"""
Module used for retrieving log entries and storing them for later analysis.
"""
import csv
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Iterable, Sequence, Tuple

from . import graylog_access
from .graylog_access import GraylogAccess

log = logging.getLogger(__name__)

# TODO make last included timestamp configurable
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


class LogRetriever:
    """
    Class used for retrieving and storing log entries.
    """

    def __init__(self, url: str, api_token: str, target_dir: str):
        self.graylog_access = GraylogAccess(url, api_token)
        self.target_dir = Path(target_dir)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} [' \
               f'graylog_access <{self.graylog_access}>]'

    def retrieve_logs(self) -> None:
        """
        Retrieves logs from the configured Graylog instance. Logs are stored
        in the configured directory grouped by their correlationID in separate
        CSV files.
        """
        self._prepare_target_dir()

        last_retrieved_timestamp = self._load_last_included_timestamp()
        first_timestamp = _get_advanced_timestamp(last_retrieved_timestamp)
        lines = self.graylog_access.get_log_entries(
            first_timestamp, EXPORTED_FIELDS)

        if not lines:
            log.info("no (new) log entries found")
            return

        fields, grouped_lines, last_timestamp = self._process_csv_lines(lines)
        self._store_logs_as_csv(grouped_lines, fields)
        self._store_last_included_timestamp(last_timestamp)

    def _prepare_target_dir(self) -> None:
        log.info('preparing target directory "%s"', self.target_dir)
        if not self.target_dir.exists():
            log.info('creating missing target directory (and parents)...')
            self.target_dir.mkdir(parents=True, exist_ok=True)

    def _load_last_included_timestamp(self) -> datetime:
        timestamp_path = self.target_dir.joinpath(TIMESTAMP_FILENAME)
        if timestamp_path.exists() and timestamp_path.is_file():
            log.info('reading last included timestamp from file "%s"',
                     timestamp_path)
            timestamp = _read_timestamp(timestamp_path)
            if graylog_access.timestamp_format_is_valid(timestamp):
                log.info('timestamp of last retrieved log entry: "%s"',
                         timestamp)
                return graylog_access.get_datetime_from_timestamp(timestamp)
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
    def _process_csv_lines(lines: List[str]) -> Tuple[
            Sequence[str], Dict[str, List[Dict[str, str]]], str]:
        reader = csv.DictReader(lines)
        sorted_list = sorted(reader, key=lambda row: row['timestamp'],
                             reverse=False)
        grouped_lines = LogRetriever._group_by_correlation_id(sorted_list)
        timestamp_of_last_entry = sorted_list[-1]['timestamp']
        return reader.fieldnames, grouped_lines, timestamp_of_last_entry

    @staticmethod
    def _group_by_correlation_id(lines: List[Dict[str, str]]) -> Dict[
            str, List[Dict[str, str]]]:
        grouped_lines = defaultdict(list)
        for line in lines:
            correlation_id = line['correlationId']
            if not correlation_id:
                log.info("omitting row with missing correlationId %s", line)
                continue
            grouped_lines[correlation_id].append(line)
        return grouped_lines

    def _store_logs_as_csv(self, grouped_dict,
                           fieldnames: Iterable[str]) -> None:
        for (correlation_id, log_entries) in grouped_dict.items():
            first_timestamp = log_entries[0]['timestamp']
            filename = f"{first_timestamp}_{correlation_id}.csv"
            file_path = self.target_dir.joinpath(filename)
            log.info("storing process with correlation_id '%s' in file '%s'",
                     correlation_id, file_path)
            with file_path.open("w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writeheader()
                writer.writerows(log_entries)
