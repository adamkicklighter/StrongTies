# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
privacy_sanitizer.py

Sanitizes and anonymizes LinkedIn-style connection CSVs for StrongTies.

Functions:
    sanitize_csv(df: pd.DataFrame, hash_ids: bool = False, obfuscate_names: bool = False, warn_on_large: int = 5000) -> pd.DataFrame
    validate_csv_columns(columns: List[str]) -> bool
"""

import pandas as pd
import unicodedata
import hashlib
from typing import List

ALLOWED_COLUMNS = ["First Name", "Last Name", "Company", "Position"]

def sanitize_csv(
    df: pd.DataFrame,
    hash_ids: bool = False,
    obfuscate_names: bool = False,
    warn_on_large: int = 5000
) -> pd.DataFrame:
    """
    Sanitize a DataFrame to ensure privacy-preserving analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame from user CSV.
    hash_ids : bool, optional
        If True, hash identifiers for anonymization.
    obfuscate_names : bool, optional
        If True, replace names with synthetic placeholders.
    warn_on_large : int, optional
        Warn if dataset exceeds this row count.

    Returns
    -------
    pd.DataFrame
        Sanitized DataFrame with only allowed columns and normalized names.
    """
    # Strip unexpected columns
    extra_cols = [col for col in df.columns if col not in ALLOWED_COLUMNS]
    if extra_cols:
        print(f"Warning: Dropping unexpected columns: {extra_cols}")
        df = df[ALLOWED_COLUMNS]

    # Normalize names
    for col in ["First Name", "Last Name"]:
        df[col] = df[col].astype(str).apply(_normalize_name)

    # Hash identifiers if requested
    if hash_ids:
        df["hash_id"] = df.apply(lambda row: _hash_identifier(row["First Name"], row["Last Name"], row["Company"]), axis=1)

    # Obfuscate names if requested
    if obfuscate_names:
        df["First Name"] = [f"Person{idx+1}" for idx in range(len(df))]
        df["Last Name"] = ["Demo" for _ in range(len(df))]

    # Validation checks
    if len(df) > warn_on_large:
        print(f"Warning: Dataset contains {len(df)} rows. Consider sampling for privacy and performance.")

    if df.isnull().any().any():
        print("Warning: Detected missing values in the dataset.")

    return df

def _normalize_name(name: str) -> str:
    """Remove accents and special characters from a name."""
    nfkd_form = unicodedata.normalize('NFKD', name)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).replace('\n', '').strip()

def _hash_identifier(first: str, last: str, company: str) -> str:
    """Hash a user's identifier for anonymization."""
    raw = f"{first.lower()}_{last.lower()}_{company.lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def validate_csv_columns(columns: List[str]) -> bool:
    """
    Check if columns match allowed fields.

    Parameters
    ----------
    columns : List[str]
        List of column names from CSV.

    Returns
    -------
    bool
        True if columns are valid, False otherwise.
    """
    return set(columns).issubset(set(ALLOWED_COLUMNS))