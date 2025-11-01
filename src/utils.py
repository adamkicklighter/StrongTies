# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
utils.py

Utility functions for StrongTies, including file/path helpers, CSV helpers, and generic data transformations.

Functions:
    ensure_dir(path: str)
    save_dataframe(df: pd.DataFrame, path: str)
    clean_company_name(name: str) -> str
    standardize_position_title(title: str) -> str
    generate_node_id(*args) -> str
"""

import os
import logging
import pandas as pd
import re
import uuid

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("strongties")

# File/path helpers
def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    logger.info(f"Ensured directory exists: {path}")

# CSV helpers
def save_dataframe(df: pd.DataFrame, path: str):
    """Save DataFrame to CSV and log info."""
    df.to_csv(path, index=False)
    logger.info(f"DataFrame saved to {path} with {len(df)} rows.")

# Generic transformations

def clean_company_name(name: str) -> str:
    """Standardize company names by removing extra spaces, punctuation, and lowercasing."""
    if not isinstance(name, str):
        return ""
    name = name.strip().lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name

def standardize_position_title(title: str) -> str:
    """Standardize position titles by lowercasing and removing common suffixes/prefixes."""
    if not isinstance(title, str):
        return ""
    title = title.strip().lower()
    title = re.sub(r'\b(senior|jr|junior|lead|head|chief|principal)\b', '', title)
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title.strip()

def generate_node_id(*args) -> str:
    """Generate a unique node ID for graphs based on input fields."""
    base = "_".join([str(a).strip().lower().replace(" ", "_") for a in args if a])
    unique = uuid.uuid5(uuid.NAMESPACE_DNS, base)
    return str(unique)

# Example usage (uncomment for script use):
# ensure_dir("results/figures")
# save_dataframe(df, "results/reports/top_connectors.csv")
# clean_company_name("  Acme, Inc. ")
# standardize_position_title("Senior Software Engineer")
# generate_node_id("John Doe", "Acme Inc", "Engineer")