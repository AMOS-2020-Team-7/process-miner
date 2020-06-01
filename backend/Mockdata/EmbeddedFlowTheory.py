import os

from pm4py.objects.log.adapters.pandas import csv_import_adapter

from pm4py.objects.conversion.log import factory as conversion_factory

from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.visualization.dfg import factory as dfg_vis_factory

from pm4py.util import constants

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_vis
from pm4py.visualization.petrinet import visualizer as petri_vis

from pm4py.objects.petri.exporter import exporter as pnml_exporter

def execute_script():
    # import csv & create log
    dataframe = csv_import_adapter.import_dataframe_from_path(datasourceMockdata(), sep=",")
    dataframe = dataframe.rename(columns={'coID': 'case:concept:name', 'Timestamp': 'time:timestamp', 'Activity': 'concept:name'})
    log = conversion_factory.apply(dataframe)

    # option 1: Directly-Follows Graph, represent frequency or performance
    parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name"}
    variant='performance'
    dfg =dfg_factory.apply(log, variant=variant, parameters=parameters)
    gviz1 = dfg_vis_factory.apply(dfg, log=log, variant=variant, parameters=parameters)
    dfg_vis_factory.view(gviz1)

    # option 2: Heuristics Miner, acts on the Directly-Follows Graph, find common structures, output: Heuristic Net (.png)
    heu_net = heuristics_miner.apply_heu(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.00})
    gviz2 = hn_vis.apply(heu_net, parameters={hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "png"})
    hn_vis.view(gviz2)

    # option 3: Petri Net based on Heuristic Miner (.svg)
    net, im, fm = heuristics_miner.apply(log, parameters={
            heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.00})
    gviz3 = petri_vis.apply(net, im, fm, parameters={petri_vis.Variants.PERFORMANCE.value.Parameters.FORMAT: "svg"}, variant=petri_vis.Variants.PERFORMANCE, log=log)
    petri_vis.view(gviz3)
    #pnml_exporter.apply(net, im, "pics/petri_embeddedFlowTheory-Frequency.pnml", final_marking=fm)

def datasourceMockdata():
    datasource = "Data/EmbeddedTheory.csv"
    return datasource


if __name__ == "__main__":
    execute_script()
