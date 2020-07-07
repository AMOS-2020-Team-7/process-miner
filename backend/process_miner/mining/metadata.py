"""
Module for extracting metadata from log data
"""
from typing import Dict

from pandas import DataFrame


def _convert_to_multi_level_dict(raw_dict):
    prepared_dict = {}
    for (first_key, second_key), count in raw_dict.items():
        prepared_dict.setdefault(first_key, {})[second_key] = count
    return prepared_dict


def get_consent_types_per_approach(frame: DataFrame):
    """
    Extracts the count of different approaches per consent type.
    :return: dict containing consent counts for each approach
    """
    raw_dict = frame.pivot_table(index=['approach', 'consent'],
                                 aggfunc='size').to_dict()
    return _convert_to_multi_level_dict(raw_dict)


def get_consent_types(frame: DataFrame):
    """
    Extracts all available consent types.
    :return: list of all available consent types
    """
    types = set()
    for value in get_consent_types_per_approach(frame).values():
        types.update(value.keys())
    return list(types)


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
    return list(get_approach_type_count(frame).keys())
