"""
Module used for importing tagged logs into
heuristic miner from retrieved_logs folder
"""
import glob
import pandas as pd


def concat_files():
    """
        all CSV files get concatenated into one file
    """
    all_filenames = glob.glob('retrieved_logs/*.csv')
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv("concatenated_files.csv",
                        index=False, encoding='utf-8-sig')
