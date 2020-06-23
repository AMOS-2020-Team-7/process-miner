"""
Utility module for working with log data in various formats
"""
import logging
from pathlib import Path
from typing import Dict

import pandas
from pandas import DataFrame
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
    assert source.is_dir()
    files = source.glob(f"*.{FILE_EXTENSION}")
    csv_files = [pandas.read_csv(file) for file in files]
    log.info('combining %s files from path %s', len(csv_files), source)
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
