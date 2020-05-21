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
dataframe = csv_import_adapter.import_dataframe_from_path("testData1.csv", sep=";")
dataframe = dataframe.rename(columns={'ID':'case:concept:name', 'Days':'time:timestamp', 'Task':'concept:name', 'Person':'org:resource'})
log = conversion_factory.apply(dataframe)

# option 1: Directly-Follows Graph, represent frequency or performance
parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name"}
variant='frequency'
dfg =dfg_factory.apply(log, variant=variant, parameters=parameters)
gviz1 = dfg_vis_factory.apply(dfg, log=log, variant=variant, parameters=parameters)
dfg_vis_factory.view(gviz1)

# option 2: Heuristics Miner, acts on the Directly-Follows Graph, find common structures, output: Heuristic Net (.svg)
heu_net = heuristics_miner.apply_heu(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
gviz2 = hn_vis.apply(heu_net , parameters={hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "svg"})
hn_vis.view(gviz2)

# option 3: Petri Net based on Heuristic Miner (.png)
net, im, fm = heuristics_miner.apply(log, parameters={
        heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
gviz3 = petri_vis.apply(net, im, fm, parameters={petri_vis.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"})
petri_vis.view(gviz3)

