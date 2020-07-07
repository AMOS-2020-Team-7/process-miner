"""
Module for preparing stored logs for data extraction
"""
from pathlib import Path

from pandas import DataFrame
from pm4py.objects.log.log import EventLog

import process_miner.mining.util.data as data_util

COLUMN_MAPPINGS = {
    'timestamp': 'time:timestamp',
    'correlationId': 'case:concept:name',
    'label': 'concept:name',
    'approach': 'case:approach'
}


class DatasetFactory:
    """
    Class for creating data sets for graph creation and metadata extraction
    """
    def __init__(self, source_directory: Path):
        self._source_directory = source_directory

    def __str__(self) -> str:
        return f'{self.__class__.__name__} [' \
               f'_source_directory <{self._source_directory}>]'

    def get_prepared_data_frame(self, approach=None, consent_type=None) \
            -> DataFrame:
        """
        Creates a DataFrame for graph creation or metadata extraction.
        :param approach: approach that should be used (all if none specified)
        :param consent_type: consent that has to be used during all sessions
        that should be considered during net creation
        :return: DataFrame representing the data set
        """
        frame = data_util.get_merged_csv_files(self._source_directory,
                                               'timestamp')
        # filter by consent
        if consent_type:
            frame = data_util.filter_related_entries(frame, 'correlationId',
                                                     'consent', [consent_type])
        # filter by approach
        if approach:
            frame = data_util.filter_by_field(frame, 'approach', approach)
        return frame

    def get_prepared_event_log(self, approach=None, consent_type=None) \
            -> EventLog:
        """
        Creates an EventLog for graph creation or metadata extraction.
        :param approach: approach that should be used (all if none specified)
        :param consent_type: consent that has to be used during all sessions
        that should be considered during net creation
        :return: EventLog representing the data set
        """
        frame = self.get_prepared_data_frame(approach, consent_type)
        data_util.rename_columns(frame, COLUMN_MAPPINGS)
        return data_util.convert_to_log(frame)
