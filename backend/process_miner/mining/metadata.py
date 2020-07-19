"""
Module for extracting metadata from log data
"""
import logging
from collections import defaultdict
from typing import Dict

from pandas import DataFrame

log = logging.getLogger(__name__)

DEFAULT_MISSING_VALUE = 'not available'


def get_sessions_per_error_type(frame: DataFrame):
    """
    Counts number of sessions each error type occurs in in the supplied
    DataFrame.
    :param frame:
    :return:
    """
    return _count_values_per_session(frame, 'errortype')


def get_sessions_per_method_type(frame: DataFrame):
    """
    Counts number of sessions each method type occurs in in the supplied
    DataFrame.
    :param frame: the DataFrame
    :return: dict containing number of occurrences
    """
    return _count_values_per_session(frame, 'method')


def get_sessions_per_bank(frame: DataFrame):
    """
    Counts number of sessions each bank occurs in in the supplied DataFrame.
    :param frame: the DataFrame
    :return: dict containing number of occurrences
    """
    return _count_values_per_session(frame, 'bank')


def _count_values_per_session(frame, column):
    counts = defaultdict(int)
    for _, session_frame in frame.groupby(['correlationId']):
        values = _get_unique_column_values(column, session_frame)
        # make sure we don't count a missing value if session has values
        if len(values) > 1:
            values.remove(DEFAULT_MISSING_VALUE)
        for value in values:
            counts[value] += 1
    return counts


def get_method_type_count_per_approach(frame: DataFrame):
    """
    Extracts the count of different approaches per method type.
    :return: dict containing method counts for each approach
    """
    methods_counts_per_approach = defaultdict(lambda: defaultdict(int))
    for session, session_frame in frame.groupby(['correlationId']):
        approaches = _get_unique_column_values('approach', session_frame)
        approach = approaches[0]
        if len(approaches) > 1:
            log.warning('more than one approach in session %s', session)
            log.warning('using first occured approach %s', approach)
        methods = _get_unique_column_values('method', session_frame)
        # make sure we don't count a missing value if session has values
        if len(methods) > 1:
            methods.remove(DEFAULT_MISSING_VALUE)
        for method in methods:
            methods_counts_per_approach[approach][method] += 1

    return dict(methods_counts_per_approach)


def get_method_types(frame: DataFrame):
    """
    Extracts all available method types.
    :return: list of all available method types
    """
    return _get_unique_column_values('method', frame)


def get_approach_type_count(frame: DataFrame) -> Dict[str, int]:
    """
    Extracts all approach types and how many sessions they each were used
    in.
    :return: dict containing the usage count per approach type
    """
    relevant_rows = frame.loc[:, ['approach', 'correlationId']]
    unique_combinations = relevant_rows.drop_duplicates()
    return unique_combinations.groupby(['approach']).size().to_dict()


def get_approach_types(frame: DataFrame):
    """
    Extracts all available approach types.
    :return: list of all available approach types
    """
    return _get_unique_column_values('approach', frame)


def _get_unique_column_values(column, frame):
    return frame[column].unique().tolist()
