"""
Tests for the log_filter module
"""
import copy

from process_miner.log_handling.log_filter import LogFilter


def _create_log_filter():
    return LogFilter(['some_field', 'filtered_field'], 'filtered_field',
                     ['^filter', '^value$'])


def test_filter_log_entries_empty():
    """
    Checks for error free processing of empty entry list.
    """
    filter_instance = _create_log_filter()
    entries = []
    filter_instance.filter_log_entries(entries)

    assert not entries


def test_filter_log_entries_no_match():
    """
    Checks if filter leaves list untouched if nothing matches.
    """
    filter_instance = _create_log_filter()
    entries = [
        {
            'some_field': 'value',
            'filtered_field': 'no filter0',
            'additional_field': ''
        },
        {
            'some_field': 'some value1',
            'filtered_field': 'no filter1'
        }
    ]
    expected_entries = copy.deepcopy(entries)
    filter_instance.filter_log_entries(entries)

    assert entries == expected_entries


def test_filter_log_entries_incomplete_entries():
    """
    Checks if filter removes incomplete entries.
    """
    filter_instance = _create_log_filter()
    entries = [
        {
            'some_field': 'value0',
            'filtered_field': 'no filter0',
            'additional_field': ''
        },
        {
            'some_field': '',
            'filtered_field': 'no filter1'
        },
        {
            'filtered_field': 'no filter2'
        }
    ]
    expected_entries = copy.deepcopy(entries[:1])
    filter_instance.filter_log_entries(entries)

    assert entries == expected_entries


def test_filter_log_entries_expression_matches():
    """
    Checks if filter removes entries matching an expression.
    """
    filter_instance = _create_log_filter()
    entries = [
        {
            'some_field': 'value0',
            'filtered_field': 'no filter0',
            'additional_field': ''
        },
        {
            'some_field': 'some value1',
            'filtered_field': 'filter1'
        }
    ]
    expected_entries = copy.deepcopy(entries[:1])
    filter_instance.filter_log_entries(entries)

    assert entries == expected_entries
