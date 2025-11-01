# SPDX-License-Identifier: Polyform-Noncommercial-1.0.0

"""
network_metrics.py

Calculates network metrics for professional social graphs.

Functions:
    compute_basic_metrics(G: nx.Graph) -> dict
    get_top_connectors(G: nx.Graph, top_n: int = 10) -> list
    detect_communities(G: nx.Graph) -> dict
"""

from typing import Dict, List, Tuple
import networkx as nx

def compute_basic_metrics(G: nx.Graph) -> Dict[str, float]:
    """
    Compute basic network metrics.

    Parameters
    ----------
    G : nx.Graph
        NetworkX graph.

    Returns
    -------
    dict
        Dictionary of metrics: number of nodes, edges, average degree, density.
    """
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = sum(dict(G.degree()).values()) / num_nodes if num_nodes > 0 else 0
    density = nx.density(G)
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "avg_degree": avg_degree,
        "density": density
    }

def get_top_connectors(G: nx.Graph, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Get the top connectors by degree.

    Parameters
    ----------
    G : nx.Graph
        NetworkX graph.
    top_n : int
        Number of top connectors to return.

    Returns
    -------
    list of tuples
        List of (node, degree) sorted by degree descending.
    """
    degree_dict = dict(G.degree())
    sorted_connectors = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_connectors[:top_n]

def detect_communities(G: nx.Graph) -> Dict[int, List[str]]:
    """
    Detect communities using the greedy modularity algorithm.

    Parameters
    ----------
    G : nx.Graph
        NetworkX graph.

    Returns
    -------
    dict
        Dictionary mapping community index to list of node names.
    """
    from networkx.algorithms.community import greedy_modularity_communities
    communities = list(greedy_modularity_communities(G))
    return {i: [str(node) for node in comm] for i, comm in enumerate(communities)}

# Example usage (uncomment for script use):
# if __name__ == "__main__":
#     import data_loader, graph_builder
#     df = data_loader.load_all_connections("../data")
#     G = graph_builder.build_connection_graph(df)
#     print(compute_basic_metrics(G))
#     print(get_top_connectors(G))
#     print(detect_communities(G))