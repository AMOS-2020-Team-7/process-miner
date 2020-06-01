import os

from pm4py.objects.log.adapters.pandas import csv_import_adapter

from pm4py.objects.conversion.log import factory as conversion_factory

from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.visualization.dfg import factory as dfg_vis_factory

from pm4py.util import constants

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_vis
from pm4py.visualization.petrinet import visualizer as petri_vis


# import csv & create log
def execute_script():
    dataframe2 = csv_import_adapter.import_dataframe_from_path(datasourceMockdata(), sep=",")
    dataframe2 = dataframe2.rename(columns={'timestamp':'time:timestamp', 'source':'case:concept:name', 'message':'concept:name'})
    log2 = conversion_factory.apply(dataframe2)

    # option 1: Heuristics Miner, acts on the Directly-Follows Graph, find common structures, output: Heuristic Net (.svg)
    heu_net = heuristics_miner.apply_heu(log2, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
    gviz2 = hn_vis.apply(heu_net , parameters={hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "svg"})
    hn_vis.view(gviz2)

    # option 2: Petri Net based on Heuristic Miner (.png)
    net, im, fm = heuristics_miner.apply(log2, parameters={
            heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
    gviz3 = petri_vis.apply(net, im, fm, parameters={petri_vis.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
    petri_vis.view(gviz3)


def datasourceMockdata():
    datasource = "../Data/graylog1.csv"
    return datasource


if __name__ == "__main__":
    execute_script()
