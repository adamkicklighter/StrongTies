# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
data_loader.py

Loads and preprocesses LinkedIn-style connection CSVs for StrongTies.

Functions:
    is_safe_path(base_dir: str, path: str) -> bool
    load_connections(csv_path: str, user_id: str, base_dir: str = None) -> pd.DataFrame
    load_all_connections(data_dir: str) -> pd.DataFrame
"""

import os
from typing import List, Optional
import pandas as pd
from privacy_sanitizer import sanitize_csv
from utils import clean_company_name, standardize_position_title

def is_safe_path(base_dir: str, path: str) -> bool:
    """
    Ensure the given path is within the base directory to prevent directory traversal attacks.
    """
    abs_base = os.path.abspath(base_dir)
    abs_path = os.path.abspath(path)
    return abs_path.startswith(abs_base)

def load_connections(csv_path: str, user_id: str, base_dir: Optional[str] = None) -> pd.DataFrame:
    """
    Load a single connections CSV file, with path validation, privacy sanitization, and user tagging.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.
    user_id : str
        Identifier for the user whose connections are in the CSV.
    base_dir : Optional[str]
        Base directory to validate the path against.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the sanitized connections data, with a user_id column.
    """
    if base_dir and not is_safe_path(base_dir, csv_path):
        raise ValueError(f"Unsafe path detected: {csv_path}")
    df = pd.read_csv(csv_path, skipinitialspace=True)
    df = sanitize_csv(df)  # Ensure privacy and allowed columns
    df = df.drop_duplicates()
    # Standardize company and position columns
    if "Company" in df.columns:
        df["Company"] = df["Company"].apply(clean_company_name)
    if "Position" in df.columns:
        df["Position"] = df["Position"].apply(standardize_position_title)
    # Concatenate First Name and Last Name into a single 'Name' column
    if "First Name" in df.columns and "Last Name" in df.columns:
        df["Name"] = df["First Name"].str.strip() + " " + df["Last Name"].str.strip()
        df = df.drop(columns=["First Name", "Last Name"])
    # Reorder columns: Name, Company, Position, user_id (if present)
    desired_order = [col for col in ["Name", "Company", "Position", "user_id"] if col in df.columns]
    other_cols = [col for col in df.columns if col not in desired_order]
    df = df[desired_order + other_cols]
    df["user_id"] = user_id
    return df

def load_all_connections(data_dir: str) -> pd.DataFrame:
    """
    Load and concatenate all connection CSVs in a directory, tagging each with its user.

    Parameters
    ----------
    data_dir : str
        Directory containing CSV files.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame of all connections, with user_id column.
    """
    abs_data_dir = os.path.abspath(data_dir)
    csv_files = [
        os.path.join(abs_data_dir, f)
        for f in os.listdir(abs_data_dir)
        if f.endswith('.csv')
    ]
    safe_csv_files = [f for f in csv_files if is_safe_path(abs_data_dir, f)]
    dfs: List[pd.DataFrame] = []
    for f in safe_csv_files:
        # Infer user_id from filename, e.g., "alice_connections.csv" -> "alice"
        basename = os.path.basename(f)
        user_id = basename.split('_')[0]
        dfs.append(load_connections(f, user_id, abs_data_dir))
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.drop_duplicates()
        return combined_df
    else:
        return pd.DataFrame()

# Example usage (uncomment for script use):
if __name__ == "__main__":
    df = load_all_connections("../StrongTies/data")
    print(df.head())
    print(df.tail())