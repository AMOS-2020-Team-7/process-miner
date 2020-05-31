"""
Tests for graylog_access module
"""
from datetime import datetime

import pytest

from process_miner.graylog_access import GraylogAccess
from process_miner.graylog_access import get_datetime_from_timestamp, \
    get_timestamp_from_datetime, timestamp_format_is_valid


def test_get_datetime_from_timestamp_invalid_timestamp_missing_characters():
    """
    Checks if invalid date raises ValueError.
    """
    with pytest.raises(ValueError):
        get_datetime_from_timestamp('2020-01-01 01:01:01.001')


def test_get_datetime_from_timestamp_valid_timestamp_default_precision():
    """
    Checks if valid date string is converted correctly.
    """
    date = datetime.fromtimestamp(0)
    assert get_datetime_from_timestamp('1970-01-01T01:00:00.000Z') == date


def test_get_datetime_from_timestamp_valid_timestamp_higher_precision():
    """
    Checks if valid date string with precision higher than required is
    converted correctly.
    """
    date = datetime.fromtimestamp(0)
    assert get_datetime_from_timestamp('1970-01-01T01:00:00.000000Z') == date


def test_get_timestamp_from_datetime():
    """
    Checks if datetime gets converted to the valid format.
    """
    date = datetime.fromisoformat('2020-01-01 01:01:01.001')
    assert get_timestamp_from_datetime(date) == '2020-01-01T01:01:01.001Z'


def test_timestamp_format_is_valid_valid_timestamp():
    """
    Checks if invalid timestamp gets recognized.
    """
    assert timestamp_format_is_valid('2020-01-01T01:01:01.001Z')


def test_timestamp_format_is_valid_invalid_timestamp():
    """
    Checks if valid timestamp gets recognized.
    """
    assert not timestamp_format_is_valid('2020-01-01 01:01:01.001')


def test___str___token_gets_redacted():
    """
    Checks if token is redacted in string representation of GraylogAccess
    object.
    """
    token = "token123"
    graylog = GraylogAccess("url", token)
    assert token not in graylog.__str__()


def test_get_log_entries_not_successful_status(requests_mock):
    """
    Checks if nothing gets returned if request was not successful.
    """
    test_url = 'http://test.test'
    requests_mock.get(f'{test_url}/api/search/universal/absolute/export',
                      status_code=404)
    graylog = GraylogAccess(test_url, 'token')
    result = graylog.get_log_entries(datetime.fromtimestamp(0), ['field1'])
    assert not result


def test_get_log_entries_successful(requests_mock):
    """
    Checks if lines get returned appropriately on successful request.
    """
    test_url = 'http://test.test'
    requests_mock.get(f'{test_url}/api/search/universal/absolute/export',
                      text='field1,field2\nvalue11,value12\nvalue21,value22')
    graylog = GraylogAccess(test_url, 'token')
    result = graylog.get_log_entries(datetime.fromtimestamp(0),
                                     ['field1,field2'])
    assert result[0] == 'field1,field2'
    assert result[1] == 'value11,value12'
    assert result[2] == 'value21,value22'
