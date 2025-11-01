# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
data_loader.py

Loads and preprocesses LinkedIn-style connection CSVs for StrongTies.

Functions:
    load_connections(csv_path: str, base_dir: str = None) -> pd.DataFrame
    load_all_connections(data_dir: str) -> pd.DataFrame
"""

import os
from typing import List, Optional
import pandas as pd

def is_safe_path(base_dir: str, path: str) -> bool:
    """
    Ensure the given path is within the base directory.
    """
    abs_base = os.path.abspath(base_dir)
    abs_path = os.path.abspath(path)
    return abs_path.startswith(abs_base)

def load_connections(csv_path: str, base_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Load a single connections CSV file, with path validation.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.
    base_dir : Optional[str]
        Base directory to validate the path against.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the connections data.
    """
    if base_dir and not is_safe_path(base_dir, csv_path):
        raise ValueError(f"Unsafe path detected: {csv_path}")
    df = pd.read_csv(csv_path, skipinitialspace=True)  # <-- Fix 1
    # Basic cleaning: drop duplicates, standardize column names
    df = df.drop_duplicates()
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    if "email" in df.columns:
        df["email"] = df["email"].str.strip()  # <-- Fix 2
    return df

def load_all_connections(data_dir: str) -> pd.DataFrame:
    """
    Load and concatenate all connection CSVs in a directory, with path validation.

    Parameters
    ----------
    data_dir : str
        Directory containing CSV files.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame of all connections.
    """
    abs_data_dir = os.path.abspath(data_dir)
    csv_files = [
        os.path.join(abs_data_dir, f)
        for f in os.listdir(abs_data_dir)
        if f.endswith('.csv')
    ]
    # Validate each file path
    safe_csv_files = [f for f in csv_files if is_safe_path(abs_data_dir, f)]
    dfs: List[pd.DataFrame] = [load_connections(f, abs_data_dir) for f in safe_csv_files]
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