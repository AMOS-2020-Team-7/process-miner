"""
Module for extracting metadata from log data
"""
import logging
from collections import defaultdict
from typing import Dict

from pandas import DataFrame

log = logging.getLogger(__name__)

DEFAULT_MISSING_VALUE = 'not available'


def get_sessions_per_consent_type(frame: DataFrame):
    """
    Counts number of session each consent type occurs in in the supplied
    DataFrame.
    :param frame: the DataFrame
    :return: dict containing number of occurrences
    """
    return _count_values_per_session(frame, 'consent')


def get_sessions_per_bank(frame: DataFrame):
    """
    Counts number of session each bank occurs in in the supplied DataFrame.
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


# TODO: look for possible code deduplication (see count_consents)
def get_consent_type_count_per_approach(frame: DataFrame):
    """
    Extracts the count of different approaches per consent type.
    :return: dict containing consent counts for each approach
    """
    consents_counts_per_approach = defaultdict(lambda: defaultdict(int))
    for session, session_frame in frame.groupby(['correlationId']):
        approaches = _get_unique_column_values('approach', session_frame)
        approach = approaches[0]
        if len(approaches) > 1:
            log.warning('more than one approach in session %s', session)
            log.warning('using first occured approach %s', approach)
        consents = _get_unique_column_values('consent', session_frame)
        # make sure we don't count a missing value if session has values
        if len(consents) > 1:
            consents.remove(DEFAULT_MISSING_VALUE)
        for consent in consents:
            consents_counts_per_approach[approach][consent] += 1

    return dict(consents_counts_per_approach)


def get_consent_types(frame: DataFrame):
    """
    Extracts all available consent types.
    :return: list of all available consent types
    """
    return _get_unique_column_values('consent', frame)


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
