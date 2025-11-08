# test_network_metrics.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
import networkx as nx

from network_metrics import compute_basic_metrics, get_top_connectors, detect_communities

def test_compute_basic_metrics_simple():
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])
    metrics = compute_basic_metrics(G)
    assert metrics["num_nodes"] == 4
    assert metrics["num_edges"] == 3
    assert pytest.approx(metrics["avg_degree"]) == 1.5
    assert 0 < metrics["density"] < 1

def test_compute_basic_metrics_empty():
    G = nx.Graph()
    metrics = compute_basic_metrics(G)
    assert metrics["num_nodes"] == 0
    assert metrics["num_edges"] == 0
    assert metrics["avg_degree"] == 0
    assert metrics["density"] == 0

def test_get_top_connectors_basic():
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")])
    top = get_top_connectors(G, top_n=2)
    assert top[0][0] == "C"  # C has highest degree
    assert top[0][1] == 3
    assert len(top) == 2

def test_get_top_connectors_less_than_top_n():
    G = nx.Graph()
    G.add_edge("A", "B")
    top = get_top_connectors(G, top_n=5)
    assert len(top) == 2

def test_get_top_connectors_empty():
    G = nx.Graph()
    top = get_top_connectors(G)
    assert top == []

def test_detect_communities_simple():
    G = nx.Graph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("D", "E")])
    communities = detect_communities(G)
    assert isinstance(communities, dict)
    # Should find 2 communities
    assert len(communities) == 2
    all_nodes = [node for comm in communities.values() for node in comm]
    assert set(all_nodes) == {"A", "B", "C", "D", "E"}

def test_detect_communities_empty():
    G = nx.Graph()
    communities = detect_communities(G)
    assert communities == {}

def test_metrics_with_isolated_nodes():
    G = nx.Graph()
    G.add_nodes_from(["A", "B", "C"])
    G.add_edge("A", "B")
    metrics = compute_basic_metrics(G)
    assert metrics["num_nodes"] == 3
    assert metrics["num_edges"] == 1
    assert metrics["avg_degree"] == pytest.approx(2/3)

def test_metrics_with_self_loops():
    G = nx.Graph()
    G.add_edge("A", "A")
    metrics = compute_basic_metrics(G)
    assert metrics["num_nodes"] == 1
    assert metrics["num_edges"] == 1
    assert metrics["avg_degree"] == 2.0  # self-loop counts as degree 2