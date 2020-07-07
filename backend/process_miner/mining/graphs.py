"""
Module for creating different graph types
"""
import logging

import pm4py.algo.discovery.dfg.algorithm as dfg_alg
import pm4py.algo.discovery.heuristics.algorithm as hn_alg
import pm4py.visualization.dfg.visualizer as dfg_vis
import pm4py.visualization.heuristics_net.visualizer as hn_vis
from pm4py.objects.log.log import EventLog
from pm4py.util import constants

log = logging.getLogger(__name__)


def create_directly_follows_graph(event_log: EventLog):
    """
    Creates a Directly Follows Graph from the supplied EventLog.
    :param event_log: the event log
    :return: object representing the created graph
    """
    parameters = {
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
        "format": "svg"
    }
    variant = 'frequency'
    graph = dfg_alg.apply(log=event_log,
                          parameters=parameters,
                          variant=variant)
    # TODO dfg breaks at this point
    return dfg_vis.apply(graph,
                         log=event_log,
                         parameters=parameters,
                         variant=variant)


def save_directly_follows_graph(graph, path):
    """
    Saves a directly-follows graph to the specified path.
    :param graph: the directly-follows graph
    :param path: the path
    """
    log.info('saving directly follows graph %s to path %s', graph, path)
    dfg_vis.save(graph, path)


def create_heuristic_net(event_log: EventLog, threshold: float = 0.0,
                         output_format: str = 'svg'):
    """
    Creates a Heuristic Net from the supplied EventLog.
    :param event_log: the EventLog
    :param threshold: the threshold to use during creation
    :param output_format: desired output format
    :return: object representing the created graph
    """
    log.info('creating heuristic net with threshold %s', threshold)
    heu_net = hn_alg.apply_heu(log=event_log, parameters={
        hn_alg.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: threshold
    })

    return hn_vis.apply(heu_net=heu_net, parameters={
        hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: output_format
    })


def save_heuristic_net(net, path):
    """
    Saves a heuristic net to the specified path.
    :param net: the heuristic net
    :param path: the path
    """
    log.info('saving heuristic net %s to path %s', net, path)
    hn_vis.save(net, path)
