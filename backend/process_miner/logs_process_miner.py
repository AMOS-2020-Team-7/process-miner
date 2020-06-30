"""
Module used for importing tagged logs into heuristic miner
"""
import os
import logging
from pathlib import Path
import glob
import pandas as pd

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


def concat_files():
    """
        all CSV files get concatenated into one file
    """
    all_filenames = glob.glob('retrieved_logs/*.csv')
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("concatenated_files.csv",
                        index=False, encoding='utf-8-sig')


def create_dataframe():
    """
    create dataframe
    """
    dataframe = csv_import_adapter.import_dataframe_from_path(
        'concatenated_files.csv', sep=",")
    dataframe = dataframe.rename(
        columns={'correlationId': 'case:concept:name',
                 'timestamp': 'time:timestamp',
                 'label': 'concept:name',
                 'approach': 'case:approach',
                 'errortype': 'case:errortype',
                 'status': 'case:status'})
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


def filter_by_errortype(errortype, dataframe):
    """
    filters dataframe by chosen error type
    """
    dataframe_errortype = attributes_filter.apply \
        (dataframe, [errortype], parameters={
            attributes_filter.Parameters.CASE_ID_KEY: "case:concept:name",
            attributes_filter.Parameters.ATTRIBUTE_KEY: "case:errortype",
            attributes_filter.Parameters.POSITIVE: True})
    return dataframe_errortype


def create_log(dataframe):
    """
    creates log out of dataframe
    """
    log = conversion_factory.apply(dataframe)
    return log


def create_graphs(without_error, log, approach):
    """
    creates visualization: Directly-Follows-Graph and Heuristic Net
    """

    # create dfg frequency
    path = "common_path"
    vis_type = "dfg_frequency"
    naming_error = "with_error"
    if without_error:
        naming_error = "no_error"
    file = f"{vis_type}_{approach}_{naming_error}.svg"
    filename = f"{path}/{vis_type}_{approach}_{naming_error}.svg"
    parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY:
                      "concept:name", "format": "svg"}
    variant = 'frequency'
    dfg = dfg_factory.apply(log, variant=variant, parameters=parameters)
    gviz = dfg_vis_factory.apply(dfg, log=log, variant=variant,
                                 parameters=parameters)
    dfg_vis_factory.view(gviz)
    dfg_vis_factory.save(gviz, filename)
    log_info.info("DFG frequency has been stored in '%s' in file '%s'",
                  path, file)

    # create dfg performance
    vis_type = "dfg_performance"
    file = f"{vis_type}_{approach}_{naming_error}.svg"
    filename = f"{path}/{vis_type}_{approach}_{naming_error}.svg"
    variant = 'performance'
    dfg = dfg_factory.apply(log, variant=variant, parameters=parameters)
    gviz = dfg_vis_factory.apply(dfg, log=log, variant=variant,
                                 parameters=parameters)
    dfg_vis_factory.view(gviz)
    dfg_vis_factory.save(gviz, filename)
    log_info.info("DFG performance has been stored in '%s' in file '%s'",
                  path, file)

    # create heuristic net
    vis_type = "heuristicnet"
    file = f"{vis_type}_{approach}_{naming_error}.svg"
    filename = f"{path}/{vis_type}_{approach}_{naming_error}.svg"
    heu_net = heuristics_miner.apply_heu(log, parameters={
        heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH:
            0.60})
    gviz = hn_vis.apply(
        heu_net, parameters={
            hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "svg"})
    hn_vis.view(gviz)
    hn_vis.save(gviz, filename)
    log_info.info("Heuristic Net has been stored in '%s' in file '%s'",
                  path, file)

    # save heuristic net in plain-ext format
    file = f"{vis_type}_{approach}_{naming_error}.plain-ext"
    filename = f"{path}/{vis_type}_{approach}_{naming_error}.plain-ext"
    gviz = hn_vis.apply(
        heu_net, parameters={
            hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "plain-ext"})
    hn_vis.save(gviz, filename)
    log_info.info("Heuristic Net as .plain-ext has been stored in '%s' "
                  "in file '%s'", path, file)

    # save heuristic net in dot format
    file = f"{vis_type}_{approach}_{naming_error}.dot"
    filename = f"{path}/{vis_type}_{approach}_{naming_error}.dot"
    gviz = hn_vis.apply(
        heu_net, parameters={
            hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "dot"})
    hn_vis.save(gviz, filename)
    log_info.info("Heuristic Net as .dot has been stored in '%s' "
                  "in file '%s'", path, file)

    # save heuristic net in xdot format
    file = f"{vis_type}_{approach}_{naming_error}.xdot"
    filename = f"{path}/{vis_type}_{approach}_{naming_error}.xdot"
    gviz = hn_vis.apply(
        heu_net, parameters={
            hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "xdot"})
    hn_vis.save(gviz, filename)
    log_info.info("Heuristic Net as .xdot has been stored in '%s' "
                  "in file '%s'", path, file)


def create_graphs_errortypes(log, errortype):
    """
    creates visualization for the error types: Heuristic Net
    """
    path = "documentation_errortypes"
    vis_type = "heuristicnet"
    filename = f"{path}/{vis_type}_{errortype}.svg"
    heu_net = heuristics_miner.apply_heu(log, parameters={
        heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH:
            0.00})
    gviz_error = hn_vis.apply(
        heu_net, parameters={
            hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "svg"})
    hn_vis.view(gviz_error)
    hn_vis.save(gviz_error, filename)


def file_available():
    """
    checks if selected file is available
    """
    file = os.path.isfile("concatenated_files.csv")
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


def filter_error(dataframe):
    """
    filter the logs with occured errors
    """
    dataframe_filtered_error = attributes_filter.apply \
        (dataframe, ["error"], parameters={
            attributes_filter.Parameters.CASE_ID_KEY: "case:concept:name",
            attributes_filter.Parameters.ATTRIBUTE_KEY: "case:status",
            attributes_filter.Parameters.POSITIVE: False})
    return dataframe_filtered_error


def create_results(without_error, approachtype, errortype):
    """
    check if concated csv file is available, filter log by selected approach,
    creates and saves DFG and Heuristic Net in directory common_path
    """
    concat_files()
    file = file_available()
    if not file:
        log_info.info('NO CONCATED FILE AVAILABLE')
        return

    valid_approach = check_selected_approach(approachtype)
    if not valid_approach:
        return

    dataframe = create_dataframe()
    dataframe_approach = filter_by_approach(approachtype, dataframe)

    if without_error:
        dataframe_approach = filter_error(dataframe_approach)

    log = create_log(dataframe_approach)
    create_graphs(without_error, log, approachtype)

    dataframe_errortype = filter_by_errortype(errortype, dataframe)
    log_errortype = create_log(dataframe_errortype)
    create_graphs_errortypes(log_errortype, errortype)


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


class Error:
    """
    class to create directory for storing error paths
    """

    def __init__(self, error_dir: str):
        self.error_dir = Path(error_dir)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} ['f'error_dir <{self.error_dir}>]'

    def prepare_graph_dir(self):
        """
        if not available, creates directory for storing the error graphs
        """
        log_info.info('preparing error graph directory "%s"', self.error_dir)
        if not self.error_dir.exists():
            log_info.info('creating missing error graph directory '
                          '(and parents)...')
            self.error_dir.mkdir(parents=True, exist_ok=True)
