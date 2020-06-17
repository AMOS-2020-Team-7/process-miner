"""
Module used for importing tagged logs into heuristic miner
"""
import os
import logging
from pathlib import Path

from pm4py.objects.log.adapters.pandas import csv_import_adapter

from pm4py.objects.conversion.log import factory as conversion_factory

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_vis

from pm4py.visualization.dfg import factory as dfg_vis_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory

from pm4py.util import constants

from pm4py.algo.filtering.pandas.attributes import attributes_filter

log_info = logging.getLogger(__name__)

POSSIBLE_APPROACHES = ["embedded", "redirect",
                       "OAuth", "all", "not available"]

APPROACH_DEFAULT = "all"


def create_dataframe():
    """
    create dataframe
    """
    dataframe = csv_import_adapter.import_dataframe_from_path(
        'concated_files.csv', sep=",")
    dataframe = dataframe.rename(
        columns={'correlationId': 'case:concept:name',
                 'timestamp': 'time:timestamp',
                 'message': 'concept:name',
                 'approach': 'case:approach'})
    return dataframe


def filter_by_approach(approach, dataframe):
    """
    dataframe gets filtered by approach
    """
    dataframe_approach = dataframe
    if approach == APPROACH_DEFAULT:
        return dataframe_approach

    dataframe_approach = attributes_filter.apply \
        (dataframe, [approach], parameters={
            attributes_filter.Parameters.CASE_ID_KEY: "case:concept:name",
            attributes_filter.Parameters.ATTRIBUTE_KEY: "case:approach",
            attributes_filter.Parameters.POSITIVE: True})
    return dataframe_approach


def create_log(dataframe):
    """
    creates log out of dataframe
    """
    log = conversion_factory.apply(dataframe)
    return log


def create_graphs(log, approach):
    """
    creates visualization: Directly-Follows-Graph and Heuristic Net
    """

    # create dfg
    path = "common_path"
    vis_type = "dfg"
    file = f"{vis_type}_{approach}.svg"
    filename = f"{path}/{vis_type}_{approach}.svg"
    parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY:
                      "concept:name", "format": "svg"}
    variant = 'frequency'
    dfg = dfg_factory.apply(log, variant=variant, parameters=parameters)
    gviz1 = dfg_vis_factory.apply(dfg, log=log, variant=variant,
                                  parameters=parameters)
    dfg_vis_factory.view(gviz1)
    dfg_vis_factory.save(gviz1, filename)
    log_info.info("DFG has been stored in '%s' in file '%s'", path, file)

    # create heuristic net
    vis_type = "heuristicnet"
    file = f"{vis_type}_{approach}.svg"
    filename = f"{path}/{vis_type}_{approach}.svg"
    heu_net = heuristics_miner.apply_heu(log, parameters={
        heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH:
            0.00})
    gviz2 = hn_vis.apply(
        heu_net, parameters={
            hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "svg"})
    hn_vis.view(gviz2)
    hn_vis.save(gviz2, filename)
    log_info.info("Heuristic Net has been stored in '%s' in file '%s'",
                  path, file)


def file_available():
    """
    checks if selected file is available
    """
    file = os.path.isfile("concated_files.csv")
    return file


def check_selected_approach(approach):
    """
    check for only valid statements for approach type
    """
    check = approach in POSSIBLE_APPROACHES
    if not check:
        log_info.info("INFO: filter by approach not possible, "
                      "no valid approach selected")
    return check


def create_results(approachtype):
    """
    check if concated csv file is available, filter log by selected approach,
    creates and saves DFG and Heuristic Net in directory common_path
    """

    file = file_available()
    if not file:
        log_info.info('NO CONCATED FILE AVAILABLE')
        return

    valid_approach = check_selected_approach(approachtype)
    if not valid_approach:
        return

    dataframe = create_dataframe()
    dataframe_approach = filter_by_approach(approachtype, dataframe)
    log = create_log(dataframe_approach)
    create_graphs(log, approachtype)


class Miner:
    """
    class to create directory for storing the graphs
    """
    def __init__(self, graph_dir: str):
        self.graph_dir = Path(graph_dir)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} ['f'graph_dir <{self.graph_dir}>]'

    def prepare_graph_dir(self):
        """
        if not available, creates directory for storing the graphs
        """
        log_info.info('preparing graph directory "%s"', self.graph_dir)
        if not self.graph_dir.exists():
            log_info.info('creating missing graph directory (and parents)...')
            self.graph_dir.mkdir(parents=True, exist_ok=True)