# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
graph_builder.py

Constructs a professional social graph from connection data.

Functions:
    build_connection_graph(df: pd.DataFrame) -> nx.Graph
"""

from typing import Optional
import pandas as pd
import networkx as nx

def build_connection_graph(df: pd.DataFrame, source_col: Optional[str] = None, target_col: Optional[str] = None) -> nx.Graph:
    """
    Build an undirected graph from a DataFrame of connections.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing connection data.
    source_col : Optional[str]
        Name of the column representing the source node (default: first column).
    target_col : Optional[str]
        Name of the column representing the target node (default: second column).

    Returns
    -------
    nx.Graph
        NetworkX graph representing the connections.
    """
    if df.empty:
        return nx.Graph()

    # Infer columns if not provided
    if source_col is None or target_col is None:
        columns = df.columns.tolist()
        if len(columns) < 2:
            raise ValueError("DataFrame must have at least two columns for source and target nodes.")
        source_col = source_col or columns[0]
        target_col = target_col or columns[1]

    G = nx.Graph()
    # Add edges from DataFrame
    for _, row in df.iterrows():
        source = row[source_col]
        target = row[target_col]
        if pd.notnull(source) and pd.notnull(target):
            G.add_edge(str(source), str(target))
    return G

# Example usage (uncomment for script use):
# if __name__ == "__main__":
#     import data_loader
#     df = data_loader.load_all_connections("../data")
#     G = build_connection_graph(df)
#     print(nx.info(G))