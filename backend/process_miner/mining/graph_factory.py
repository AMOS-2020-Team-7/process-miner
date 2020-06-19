"""
Module for creating different graph types
"""
from pathlib import Path

import pm4py.algo.discovery.dfg.algorithm as dfg_alg
import pm4py.algo.discovery.heuristics.algorithm as hn_alg
import pm4py.visualization.dfg.visualizer as dfg_vis
import pm4py.visualization.heuristics_net.visualizer as hn_vis
from pm4py.objects.log.log import EventLog
from pm4py.util import constants

import process_miner.mining.util.data as data_util

COLUMN_MAPPINGS = {
    'timestamp': 'time:timestamp',
    'correlationId': 'case:concept:name',
    'message': 'concept:name',
    'approach': 'case:approach'
}


def create_directly_follows_graph(log: EventLog):
    """
    Creates a Directly Follows Graph from the supplied EventLog.
    :param log: the event log
    :return: object representing the created graph
    """
    parameters = {
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
        "format": "svg"
    }
    variant = 'frequency'
    # TODO dfg breaks at this point
    graph = dfg_alg.apply(log=log,
                          parameters=parameters,
                          variant=variant)
    visualization = dfg_vis.apply(graph,
                                  log=log,
                                  parameters=parameters,
                                  variant=variant)

    return visualization


def create_heuristic_net(log: EventLog, threshold: float = 0.00):
    """
    Creates a Heuristic Net from the supplied EventLog.
    :param log: the EventLog
    :param threshold: the threshold to use during creation
    :return: object representing the created graph
    """
    heu_net = hn_alg.apply_heu(log=log, parameters={
        hn_alg.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: threshold
    })

    return hn_vis.apply(heu_net=heu_net, parameters={
        hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: 'svg'
    })


class GraphFactory:
    """
    Class for creating different graphs from the data contained in a directory
    """
    def __init__(self, source_directory: Path):
        self._source_directory = source_directory

    def get_directly_follows_graph(self):
        """
        Creates a Directly Follows Graph from the available data.
        :return: object representing the created graph
        """
        event_log = self._get_prepared_event_log()
        return create_directly_follows_graph(event_log)

    def get_heuristic_net(self, threshold: float = 0.00):
        """
        Creates a Heuristic Net from the available data.
        :param threshold: the threshold to use during creation
        :return: object representing the created graph
        """
        event_log = self._get_prepared_event_log()
        return create_heuristic_net(event_log, threshold)

    def _get_prepared_event_log(self):
        frame = data_util.get_merged_csv_files(self._source_directory)
        data_util.rename_columns(frame, COLUMN_MAPPINGS)
        return data_util.convert_to_log(frame)
