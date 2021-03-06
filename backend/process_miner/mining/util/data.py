"""
Utility module for working with log data in various formats
"""
import logging
from pathlib import Path
from typing import Dict, List

import pandas
from pandas import DataFrame
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.objects.conversion.log import factory as event_log_factory
from pm4py.objects.log.log import EventLog

log = logging.getLogger(__name__)

FILE_EXTENSION = 'csv'


def get_merged_csv_files(source: Path, sort_column: str = None) -> DataFrame:
    """
    Converts all CSV files found at the specified path to a single DataFrame
    and optionally sorts by the specified column.
    :param source: the path to the directory containing the CSV files
    :param sort_column: column the resulting DataFrame should be sorted by
    :return: the resulting DataFrame
    """
    csv_files = get_csv_files(source)
    return merge_and_sort_dataframes(csv_files, sort_column)


def get_csv_files(source: Path) -> List[DataFrame]:
    """
    Reads all CSV files from the specified path to DataFrames.
    :param source: the source directory
    :return: a list containing the DataFrames
    """
    if not source.is_dir():
        log.error('%s is not a directory', source)
        raise Exception()
    files = source.glob(f"*.{FILE_EXTENSION}")
    return [pandas.read_csv(file) for file in files]


def merge_and_sort_dataframes(csv_files: List[DataFrame],
                              sort_column: str = None) -> DataFrame:
    """
    Merges the supplied DataFrames into a single DataFrame and optionally sorts
    them by the supplied column.
    :param csv_files: the initial DataFrames
    :param sort_column: the column to sort by
    :return: the resulting DataFrame
    """
    log.info('combining %s files', len(csv_files))
    frame = pandas.concat(csv_files)
    if not sort_column:
        return frame
    log.info('sorting by column "%s"', sort_column)
    return frame.sort_values(sort_column)


def rename_columns(frame: DataFrame, mapping: Dict[str, str]):
    """
    Renames columns of the supplied DataFrame according to the supplied
    mapping.
    :param frame: the DataFrame
    :param mapping: the mapping
    """
    log.info('renaming columns with mapping %s', mapping)
    frame.rename(columns=mapping, inplace=True)


def convert_to_log(frame: DataFrame) -> EventLog:
    """
    Converts a DataFrame to an EventLog.
    :param frame: the DataFrame
    :return: the resulting EventLog
    """
    return event_log_factory.apply(frame)


def filter_by_field(frame: DataFrame, field: str, value: str) -> DataFrame:
    """
    Filters given DataFrame.
    :param frame: the DataFrame
    :param field: the field that the filter should be applied on
    :param value: the value that is expected in the filter field
    :return: a DataFrame representing a filtered view of the original DataFrame
    """
    log.info('filtering log entries by value "%s" on field "%s"', value, field)
    return frame.loc[frame[field] == value]


def dataframe_has_value_in_column(frame: DataFrame, column: str, value: str) \
        -> DataFrame:
    """
    Determines if a column of a DataFrame contains a value.
    :param frame: the DataFrame
    :param column: the column
    :param value: the value that should occur in that column
    :return: whether the value was found in the column
    """
    return value in frame[column].values


def filter_related_entries(frame: DataFrame, session_field: str,
                           attribute_field: str, values: List[str],
                           keep: bool = True) -> DataFrame:
    """
    Filters related entries from a DataFrame based on the values of one of the
    entries fields.
    :param frame: the DataFrame
    :param session_field: the field that marks related entries
    :param attribute_field: the field that should be checked for desired values
    :param values: the desired values
    :param keep: whether the matching entries or non-matching entries should
    be kept
    :return: a filtered representation of the initial DataFrame
    """
    parameters = {
        attributes_filter.Parameters.CASE_ID_KEY: session_field,
        attributes_filter.Parameters.ATTRIBUTE_KEY: attribute_field,
        attributes_filter.Parameters.POSITIVE: keep
    }
    return attributes_filter.apply(frame, values, parameters=parameters)
