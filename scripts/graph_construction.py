# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

import sys
import os
import argparse
import networkx as nx

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.target_preferences import TargetPreferences
from src.data_loader import load_all_connections
from src.graph_builder import build_connection_graph

def main(data_dir: str, output_path: str, targets_path: str = None) -> None:
    """
    Construct a professional social graph from user connection data and save as GraphML.

    Parameters
    ----------
    data_dir : str
        Directory containing connection CSV files.
    output_path : str
        Path to save the output GraphML file.
    targets_path : str, optional
        Path to JSON file with target companies and roles.

    Returns
    -------
    None
    """
    df = load_all_connections(data_dir)
    G = build_connection_graph(df, source_col="user_id", target_col="name")

    # Load target preferences if provided
    target_prefs = None
    if targets_path and os.path.exists(targets_path):
        import json
        with open(targets_path, "r") as f:
            prefs = json.load(f)
        target_prefs = TargetPreferences(prefs.get("companies", []), prefs.get("roles", []))

        # Annotate nodes with target match info
        for node, data in G.nodes(data=True):
            if target_prefs.matches(data):
                G.nodes[node]["is_target"] = True
            else:
                G.nodes[node]["is_target"] = False

    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Ensure the results directory exists
    results_dir = os.path.dirname(output_path)
    if results_dir and not os.path.exists(results_dir):
        os.makedirs(results_dir, exist_ok=True)

    nx.write_graphml(G, output_path)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Construct and save a professional social graph."
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="data",
        help="Directory with connection CSVs"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/figures/network.graphml",
        help="Output graph file"
    )
    parser.add_argument(
        "--targets",
        type=str,
        default=None,
        help="Path to JSON file with target companies and roles"
    )
    args = parser.parse_args()
    main(args.data_dir, args.output, args.targets)