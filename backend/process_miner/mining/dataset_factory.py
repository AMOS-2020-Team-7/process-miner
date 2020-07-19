"""
Module for preparing stored logs for data extraction
"""
from pathlib import Path

from pandas import DataFrame

import process_miner.mining.util.data as data_util


class DatasetFactory:
    """
    Class for creating data sets for graph creation and metadata extraction
    """
    def __init__(self, source_directory: Path):
        self._source_directory = source_directory

    def __str__(self) -> str:
        return f'{self.__class__.__name__} [' \
               f'_source_directory <{self._source_directory}>]'

    def get_prepared_data_frame(self, approach=None, method_type=None,
                                error_type=None) -> DataFrame:
        """
        Creates a DataFrame for graph creation or metadata extraction.
        :param approach: approach that should be used (all if none specified)
        :param method_type: method that has to be used during all sessions
        that should be included
        :return: DataFrame representing the data set
        """
        frame = data_util.get_merged_csv_files(self._source_directory,
                                               'timestamp')
        # filter by method
        if method_type:
            frame = data_util.filter_related_entries(frame, 'correlationId',
                                                     'method', [method_type])
        # filter by approach
        if approach:
            frame = data_util.filter_by_field(frame, 'approach', approach)

        # filter by method
        if error_type:
            frame = data_util.filter_related_entries(frame, 'correlationId',
                                                     'errortype', [error_type])
        return frame
