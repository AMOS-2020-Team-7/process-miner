import datetime
import logging
import requests
from pathlib import Path
from urllib.parse import urljoin

log = logging.getLogger(__name__)

default_oldest_retrieved_timestamp = "1970-01-01T01:00:00.000Z"
oldest_retrieved_timestamp_filename = "oldest_timestamp"

absolute_search_path = "api/search/universal/absolute"
default_headers = {'Accept': 'application/json'}
default_query_parameters = {'query': '*', 'fields': 'correlationId, message, timestamp', 'limit': '10', 'pretty': 'true'}


def timestamp_is_valid(timestamp: str) -> bool:
    try:
        datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        return False


def read_timestamp(path: Path) -> str:
    with path.open('r') as file:
        return file.readline(len(default_oldest_retrieved_timestamp))


class LogRetriever:
    def __init__(self, url: str, api_token: str, target_dir: str):
        self.url = urljoin(url, absolute_search_path)
        self.api_token = api_token
        self.target_dir = Path(target_dir)

    def download_logs(self) -> None:
        self.__prepare_target_dir()
        self.__init_oldest_timestamp()

        query_parameters = self.__prepare_query_parameters()
        log.info("retrieving logs in time range from '%s' to '%s' via GET request to %s", self.oldest_timestamp,
                 query_parameters['to'], self.url)
        response = requests.get(self.url, headers=default_headers, auth=(self.api_token, 'token'), params=query_parameters)

        if response.status_code != 200:
            log.error("log retrieval failed with status code '%s', reason '%s' and body \n%s", response.status_code, response.reason, response.text)
            return

        # TODO actual log storage (and possibly grouping by correlationId)
        print(response.text)
        # TODO store 'to' timestamp

    def __prepare_target_dir(self) -> None:
        log.info("checking access to target directory '%s'...", self.target_dir)
        if not self.target_dir.exists():
            log.info("creating missing target directory (and parents)...")
            self.target_dir.mkdir(parents=True, exist_ok=True)
        log.info("...success")

    def __init_oldest_timestamp(self) -> None:
        oldest_timestamp_path = self.target_dir.joinpath(oldest_retrieved_timestamp_filename)
        if oldest_timestamp_path.exists() and oldest_timestamp_path.is_file():
            log.info("reading oldest timestamp from file '%s'", oldest_timestamp_path)
            timestamp = read_timestamp(oldest_timestamp_path)
            if timestamp_is_valid(timestamp):
                self.oldest_timestamp = timestamp
                log.info("oldest timestamp in target directory: '%s'", timestamp)
                return
            else:
                log.error("invalid timestamp '%s'...", timestamp)
        else:
            log.info("information about oldest timestamp not found in target directory...")

        log.info("...using default timestamp '%s'", default_oldest_retrieved_timestamp)
        self.oldest_timestamp = default_oldest_retrieved_timestamp

    def __prepare_query_parameters(self):
        query_parameters = default_query_parameters.copy()
        query_parameters['from'] = self.oldest_timestamp
        # TODO proper time formating without string manipulation
        query_parameters['to'] = str(datetime.datetime.now())[:-3]
        return query_parameters
