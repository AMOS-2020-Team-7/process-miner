"""
Module for extracting metadata from log data
"""
from pathlib import Path
from typing import Dict

import process_miner.mining.util.data as data_util


def _convert_to_multi_level_dict(raw_dict):
    prepared_dict = {}
    for (first_key, second_key), count in raw_dict.items():
        prepared_dict.setdefault(first_key, {})[second_key] = count
    return prepared_dict


class MetadataFactory:
    """
    Class for extracting metadata from the data contained in a directory
    """
    def __init__(self, source_directory: Path):
        self._source_directory = source_directory

    def get_consent_types_per_approach(self) -> Dict[str, Dict[str, int]]:
        """
        Extracts the count of different approaches per consent type.
        :return: dict containing consent counts for each approach
        """
        frame = data_util.get_merged_csv_files(self._source_directory)
        raw_dict = frame.pivot_table(index=['approach', 'consent'],
                                     aggfunc='size').to_dict()
        return _convert_to_multi_level_dict(raw_dict)

    def get_consent_types(self):
        """
        Extracts all available consent types.
        :return: list of all available consent types
        """
        types = set()
        for value in self.get_consent_types_per_approach().values():
            types.update(value.keys())
        return list(types)

    def get_approach_type_count(self) -> Dict[str, int]:
        """
        Extracts all approach types and how many sessions they each were used
        in.
        :return: dict containing the usage count per approach type
        """
        frame = data_util.get_merged_csv_files(self._source_directory)
        relevant_rows = frame.loc[:, ['approach', 'correlationId']]
        unique_combinations = relevant_rows.drop_duplicates()
        return unique_combinations.groupby(['approach']).size().to_dict()

    def get_approach_types(self):
        """
        Extracts all available approach types.
        :return: list of all available approach types
        """
        return list(self.get_approach_type_count().keys())
