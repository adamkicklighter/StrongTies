# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
visualization.py

Visualizes professional social graphs and network analysis results.

Functions:
    plot_network(G: nx.Graph, filename: str = None) -> None
    plot_communities(G: nx.Graph, communities: dict, filename: str = None) -> None
"""

from typing import Optional, Dict
import matplotlib.pyplot as plt
import networkx as nx

def plot_network(G: nx.Graph, filename: Optional[str] = None) -> None:
    """
    Plot the entire network graph.

    Parameters
    ----------
    G : nx.Graph
        NetworkX graph to visualize.
    filename : Optional[str]
        If provided, save the plot to this file.
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='skyblue', edge_color='gray', font_size=8)
    plt.title("Professional Social Network")
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300)
    plt.show()

def plot_communities(G: nx.Graph, communities: Dict[int, list], filename: Optional[str] = None) -> None:
    """
    Plot the network graph with nodes colored by community.

    Parameters
    ----------
    G : nx.Graph
        NetworkX graph to visualize.
    communities : dict
        Dictionary mapping community index to list of node names.
    filename : Optional[str]
        If provided, save the plot to this file.
    """
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    # Assign a color to each community
    import itertools
    colors = itertools.cycle(plt.cm.tab10.colors)
    node_color_map = {}
    for idx, nodes in communities.items():
        color = next(colors)
        for node in nodes:
            node_color_map[node] = color
    node_colors = [node_color_map.get(node, (0.5, 0.5, 0.5)) for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_size=300, node_color=node_colors, edge_color='gray', font_size=8)
    plt.title("Network Communities")
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300)
    plt.show()

# Example usage (uncomment for script use):
# if __name__ == "__main__":
#     import data_loader, graph_builder, network_metrics
#     df = data_loader.load_all_connections("../data")
#     G = graph_builder.build_connection_graph(df)
#     plot_network(G, filename="../results/figures/network_overview.png")
#     communities = network_metrics.detect_communities(G)
#     plot_communities(G, communities, filename="../results/figures/cluster_analysis.png")