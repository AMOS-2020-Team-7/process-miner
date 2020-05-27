import csv
import logging
import requests
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Sequence, Dict, Iterable
from urllib.parse import urljoin


log = logging.getLogger(__name__)

# TODO make last included timestamp configurable
default_last_included_timestamp = "1970-01-01T01:00:00.000Z"
last_included_timestamp_filename = "last_included_timestamp"
GRAYLOG_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

absolute_search_api_path = "api/search/universal/absolute/export"
default_headers = {'Accept': 'text/csv'}
default_query_parameters = {'query': "*", 'fields': "correlationId, timestamp, message", 'batch_size': 0}


def timestamp_is_valid(timestamp: str) -> bool:
    try:
        datetime.strptime(timestamp, GRAYLOG_TIMESTAMP_FORMAT)
        return True
    except ValueError:
        return False


def get_advanced_timestamp(timestamp: str) -> str:
    advanced_timestamp = datetime.strptime(timestamp, GRAYLOG_TIMESTAMP_FORMAT) + timedelta(milliseconds=1)
    return get_graylog_formatted_timestamp(advanced_timestamp)


def get_graylog_formatted_timestamp(advanced_timestamp: datetime) -> str:
    # TODO proper time formatting without string manipulation
    return datetime.strftime(advanced_timestamp, GRAYLOG_TIMESTAMP_FORMAT)[:-4] + "Z"


def read_timestamp(path: Path) -> str:
    with path.open('r') as file:
        return file.readline()


class LogRetriever:
    def __init__(self, url: str, api_token: str, target_dir: str):
        self.url = urljoin(url, absolute_search_api_path)
        self.api_token = api_token
        self.target_dir = Path(target_dir)

    def retrieve_logs(self) -> None:
        self.__prepare_target_dir()
        self.__load_last_included_timestamp()

        response = self.query_graylog()
        if response.status_code != 200:
            log.error("log retrieval failed with status code '%s', reason '%s' and response body \n%s",
                      response.status_code, response.reason, response.text)
            return

        lines = response.text.splitlines()
        if not lines:
            log.info("no (new) log entries found")
            return

        fieldnames, grouped_lines, newest_timestamp = self.process_csv_lines(lines)
        self.__store_logs_as_csv(grouped_lines, fieldnames)
        self.__store_last_included_timestamp(newest_timestamp)

    def __prepare_target_dir(self) -> None:
        log.info("checking access to target directory '%s'...", self.target_dir)
        if not self.target_dir.exists():
            log.info("creating missing target directory (and parents)...")
            self.target_dir.mkdir(parents=True, exist_ok=True)
        log.info("...success")

    def __load_last_included_timestamp(self) -> None:
        last_included_timestamp_path = self.target_dir.joinpath(last_included_timestamp_filename)
        if last_included_timestamp_path.exists() and last_included_timestamp_path.is_file():
            log.info("reading last included timestamp from file '%s'", last_included_timestamp_path)
            timestamp = read_timestamp(last_included_timestamp_path)
            if timestamp_is_valid(timestamp):
                self.first_included_timestamp = get_advanced_timestamp(timestamp)
                log.info("timestamp of last included log entry in target directory: '%s'", timestamp)
                return
            else:
                log.error("invalid timestamp format '%s'...", timestamp)
        else:
            log.info("information about last included timestamp not found in target directory...")

        log.info("...using default timestamp '%s'", default_last_included_timestamp)
        self.first_included_timestamp = default_last_included_timestamp

    def query_graylog(self) -> requests.Response:
        query_parameters = self.__get_query_parameters()
        log.info("retrieving logs in time range from '%s' to '%s' via GET request to %s", self.first_included_timestamp,
                 query_parameters['to'], self.url)
        return requests.get(self.url, headers=default_headers, auth=(self.api_token, 'token'), params=query_parameters)

    def __get_query_parameters(self) -> str:
        query_parameters = default_query_parameters.copy()
        query_parameters['from'] = self.first_included_timestamp
        query_parameters['to'] = get_graylog_formatted_timestamp(datetime.now())
        return query_parameters

    @staticmethod
    def process_csv_lines(lines: List[str]):
        reader = csv.DictReader(lines)
        sorted_list = sorted(reader, key=lambda row: row['timestamp'], reverse=False)
        grouped_dict = LogRetriever.group_lines_by_correlation_id(sorted_list)
        newest_timestamp = sorted_list[-1]['timestamp']
        return reader.fieldnames, grouped_dict, newest_timestamp

    @staticmethod
    def group_lines_by_correlation_id(lines: List[Dict[str, str]]):
        grouped_dict = defaultdict(list)
        for line in lines:
            correlation_id = line['correlationId']
            if not correlation_id:
                log.info("omitting row with missing correlationId %s", line)
                continue
            grouped_dict[correlation_id].append(line)
        return grouped_dict

    def __store_logs_as_csv(self, grouped_dict, fieldnames: Iterable[str]) -> None:
        for (k, v) in grouped_dict.items():
            filename = "{}_{}.csv".format(v[0]['timestamp'], k)
            file_path = self.target_dir.joinpath(filename)
            log.info("storing process with correlationId '%s' in file '%s'", k, file_path)
            with file_path.open("w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames)
                writer.writeheader()
                writer.writerows(v)

    def __store_last_included_timestamp(self, timestamp: str) -> None:
        timestamp_path = self.target_dir.joinpath(last_included_timestamp_filename)
        with timestamp_path.open("w") as timestamp_file:
            log.info("storing timestamp of last included log entry in file '%s'", timestamp_path)
            timestamp_file.write(timestamp)
