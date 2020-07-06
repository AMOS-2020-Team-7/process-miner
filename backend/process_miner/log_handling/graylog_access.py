"""
Module responsible for log retrieval from Graylog. The communication with
Graylog is done by the class GraylogAccess. The module also provides methods
for converting datetime objects from and to timestamp strings in a format
accepted by Graylog.
"""
import logging
from datetime import datetime
from typing import Dict, List
from urllib.parse import urljoin

import requests

log = logging.getLogger(__name__)

GRAYLOG_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

_ABS_SEARCH_API_PATH = 'api/search/universal/absolute/export'
_ABS_SEARCH_DEFAULT_HEADERS = {'Accept': 'text/csv'}
_ABS_SEARCH_DEFAULT_QUERY_PARAMS = {'query': '*', 'batch_size': 0}


def get_datetime_from_timestamp(timestamp: str) -> datetime:
    """
    Get datetime representation of timestamp string in Graylog format.

    :param timestamp: timestamp in Graylog format
    :return: datetime representation of the timestamp
    """
    return datetime.strptime(timestamp, GRAYLOG_TIMESTAMP_FORMAT)


def get_timestamp_from_datetime(timestamp: datetime) -> str:
    """
    Get Graylog formatted string representation of a datetime object.

    :param timestamp: datetime representation of the timestamp
    :return: timestamp in Graylog format
    """
    return timestamp.strftime(GRAYLOG_TIMESTAMP_FORMAT)[:-4] + 'Z'


def timestamp_format_is_valid(timestamp: str) -> bool:
    """
    Determines if the supplied timestamp is valid for usage with Graylog.

    :param timestamp: timestamp that is to be checked
    :return: whether the timestamp is valid (True) or invalid (False)
    """
    try:
        get_datetime_from_timestamp(timestamp)
    except ValueError:
        return False

    return True


def _get_absolute_search_query_parameters(since: datetime, fields: List[str]) \
        -> Dict[str, str]:
    query_parameters = dict(_ABS_SEARCH_DEFAULT_QUERY_PARAMS)
    query_parameters['from'] = get_timestamp_from_datetime(since)
    query_parameters['to'] = get_timestamp_from_datetime(datetime.now())
    query_parameters['fields'] = ','.join(fields)
    return query_parameters


class GraylogAccess:
    """
    Provides access to the REST-API provided by Graylog.
    """
    def __init__(self, url: str, api_token: str):
        self.url = url
        self.api_token = api_token

    def __str__(self) -> str:
        return f'{self.__class__.__name__} [url <{self.url}> api_token ' \
               f'<*{self.api_token[1:4]}******>'  # don't use full token

    def get_log_entries(self, since: datetime, fields: List[str]) -> List[str]:
        """
        Exports all log entries since the supplied supplied datetime in CSV
        format. The names of the retrieved fields will be used as column names.

        :param since: earliest possible time of log entry occurrence
        :param fields: name of the fields that should get retrieved
        :return: list of strings with one entry pre CSV formatted line
        """
        response = self._execute_absolute_search(since, fields)
        if response.status_code != 200:
            log.error('log retrieval failed with status code "%s", reason "%s"'
                      ' and response body \n%s',
                      response.status_code, response.reason, response.text)
            return None

        return response.text.splitlines()

    def _execute_absolute_search(self, since: datetime, fields: List[str])\
            -> requests.Response:
        url = urljoin(self.url, _ABS_SEARCH_API_PATH)
        query_parameters = _get_absolute_search_query_parameters(since, fields)
        log.info(
            'retrieving logs in time range from "%s" to "%s" via GET request'
            ' to %s',
            query_parameters['from'], query_parameters['to'], self.url
        )
        return requests.get(
            url,
            headers=_ABS_SEARCH_DEFAULT_HEADERS,
            auth=(self.api_token, 'token'),
            params=query_parameters
        )
