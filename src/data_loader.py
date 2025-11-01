# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
data_loader.py

Loads and preprocesses LinkedIn-style connection CSVs for StrongTies.

Functions:
    load_connections(csv_path: str) -> pd.DataFrame
    load_all_connections(data_dir: str) -> pd.DataFrame
"""

import os
from typing import List
import pandas as pd

def load_connections(csv_path: str) -> pd.DataFrame:
    """
    Load a single connections CSV file.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the connections data.
    """
    df = pd.read_csv(csv_path)
    # Basic cleaning: drop duplicates, standardize column names
    df = df.drop_duplicates()
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df

def load_all_connections(data_dir: str) -> pd.DataFrame:
    """
    Load and concatenate all connection CSVs in a directory.

    Parameters
    ----------
    data_dir : str
        Directory containing CSV files.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame of all connections.
    """
    csv_files = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith('.csv')
    ]
    dfs: List[pd.DataFrame] = [load_connections(f) for f in csv_files]
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.drop_duplicates()
        return combined_df
    else:
        return pd.DataFrame()

# Example usage (uncomment for script use):
# if __name__ == "__main__":
#     df = load_all_connections("../data")
#     print(df.head())