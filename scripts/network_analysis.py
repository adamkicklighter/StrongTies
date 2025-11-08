# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import pandas as pd
import networkx as nx
from src.target_preferences import TargetPreferences

from src.network_metrics import compute_basic_metrics, get_top_connectors, detect_communities

def main(graph_path: str, output_dir: str, targets_path: str = None) -> None:
    """
    Analyze a professional social network graph and output metrics, top connectors, and community assignments.

    Parameters
    ----------
    graph_path : str
        Path to the input GraphML file.
    output_dir : str
        Directory to save output reports.
    targets_path : str
        Path to JSON file with target companies and roles.

    Returns
    -------
    None
    """
    # Load the graph
    print(f"Loading graph from {graph_path}...")
    G = nx.read_graphml(graph_path)
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load target preferences if provided
    target_prefs = None
    if targets_path and os.path.exists(targets_path):
        import json
        with open(targets_path, "r") as f:
            prefs = json.load(f)
        target_prefs = TargetPreferences(prefs.get("companies", []), prefs.get("roles", []))

    # Compute basic metrics
    print("\nComputing basic network metrics...")
    metrics = compute_basic_metrics(G)
    print(f"Number of nodes: {metrics['num_nodes']}")
    print(f"Number of edges: {metrics['num_edges']}")
    print(f"Average degree: {metrics['avg_degree']:.2f}")
    print(f"Network density: {metrics['density']:.4f}")

    # Save basic metrics
    metrics_df = pd.DataFrame([metrics])
    metrics_path = os.path.join(output_dir, "network_metrics.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"Basic metrics saved to {metrics_path}")

    # Get top connectors
    print("\nIdentifying top connectors...")
    top_connectors = get_top_connectors(G, top_n=20)
    connectors_df = pd.DataFrame(top_connectors, columns=["name", "degree"])
    connectors_path = os.path.join(output_dir, "top_connectors.csv")
    connectors_df.to_csv(connectors_path, index=False)
    print(f"Top 20 connectors saved to {connectors_path}")
    print("\nTop 10 connectors:")
    for name, degree in top_connectors[:10]:
        print(f"  {name}: {degree} connections")

    # Detect communities
    print("\nDetecting communities...")
    communities = detect_communities(G)
    print(f"Found {len(communities)} communities")

    # Save community information
    community_data = []
    for comm_id, members in communities.items():
        for member in members:
            community_data.append({"community_id": comm_id, "name": member})

    communities_df = pd.DataFrame(community_data)
    communities_path = os.path.join(output_dir, "communities.csv")
    communities_df.to_csv(communities_path, index=False)
    print(f"Community assignments saved to {communities_path}")

    # Print community summary
    print("\nCommunity summary:")
    for comm_id, members in sorted(communities.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
        print(f"  Community {comm_id}: {len(members)} members")

    # Report target matches
    if target_prefs:
        print("\nConnections matching target companies/roles:")
        target_nodes = []
        for node, data in G.nodes(data=True):
            if target_prefs.matches(data):
                target_nodes.append(node)
        if target_nodes:
            print(f"  {len(target_nodes)} connections")
            for node in target_nodes[:10]:
                print(f"  {node} ({G.nodes[node].get('company', '')}, {G.nodes[node].get('role', '')})")

    # Identify connectors to targets
    if target_prefs:
        print("\nRanking connectors by target relevance...")
        connector_target_matches = []
        for name, degree in top_connectors:
            node_data = G.nodes[name]
            matches_target = target_prefs.matches(node_data)
            connector_target_matches.append({
                "name": name,
                "degree": degree,
                "matches_target": matches_target,
                "company": node_data.get("company", ""),
                "role": node_data.get("role", "")
            })
        # Save connectors with target relevance
        target_connectors_df = pd.DataFrame(connector_target_matches)
        target_connectors_path = os.path.join(output_dir, "target_connectors.csv")
        target_connectors_df.to_csv(target_connectors_path, index=False)
        print(f"Connector relevance to targets saved to {target_connectors_path}")

    print(f"\nAnalysis complete. All results saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze professional social network metrics."
    )
    parser.add_argument(
        "--graph",
        type=str,
        default="results/figures/network.graphml",
        help="Path to input graph file"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="results/reports",
        help="Directory for output reports"
    )
    parser.add_argument(
        "--targets",
        type=str,
        default=None,
        help="Path to JSON file with target companies and roles"
    )
    args = parser.parse_args()
    main(args.graph, args.output_dir, args.targets)