import glob
import pandas as pd
from pm4py.objects.log.adapters.pandas import csv_import_adapter

from pm4py.objects.conversion.log import factory as conversion_factory

from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_vis


def concat_files():
    all_filenames = [i for i in glob.glob('retrieved_logs/'+'*.csv')]
    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv("concated_files.csv", index=False, encoding='utf-8-sig')

def execute_script():
    # import csv & create log
    dataframe = csv_import_adapter.import_dataframe_from_path('concated_files.csv', sep=",")
    dataframe = dataframe.rename(columns={'correlationId': 'case:concept:name', 'timestamp': 'time:timestamp', 'message': 'concept:name'})
    log = conversion_factory.apply(dataframe)

    heu_net = heuristics_miner.apply_heu(log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.00})
    gviz2 = hn_vis.apply(heu_net, parameters={hn_vis.Variants.PYDOTPLUS.value.Parameters.FORMAT: "png"})
    hn_vis.view(gviz2)