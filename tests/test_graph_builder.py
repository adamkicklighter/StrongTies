import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
import pandas as pd
import networkx as nx

from graph_builder import build_connection_graph

def test_build_connection_graph_basic():
    df = pd.DataFrame({
        "source": ["A", "B", "C"],
        "target": ["B", "C", "D"]
    })
    G = build_connection_graph(df, "source", "target")
    assert isinstance(G, nx.Graph)
    assert set(G.nodes) == {"A", "B", "C", "D"}
    assert set(G.edges) == {("A", "B"), ("B", "C"), ("C", "D")}

def test_build_connection_graph_infer_columns():
    df = pd.DataFrame({
        "foo": ["X", "Y"],
        "bar": ["Y", "Z"]
    })
    G = build_connection_graph(df)
    assert set(G.nodes) == {"X", "Y", "Z"}
    assert set(G.edges) == {("X", "Y"), ("Y", "Z")}

def test_build_connection_graph_empty_df():
    df = pd.DataFrame(columns=["source", "target"])
    G = build_connection_graph(df)
    assert isinstance(G, nx.Graph)
    assert len(G.nodes) == 0
    assert len(G.edges) == 0

def test_build_connection_graph_less_than_two_columns():
    df = pd.DataFrame({"only_one": ["A", "B"]})
    with pytest.raises(ValueError):
        build_connection_graph(df)

def test_build_connection_graph_null_values():
    df = pd.DataFrame({
        "source": ["A", None, "C"],
        "target": ["B", "C", None]
    })
    G = build_connection_graph(df, "source", "target")
    assert set(G.nodes) == {"A", "B"}
    assert set(G.edges) == {("A", "B")}

def test_build_connection_graph_node_type_is_str():
    df = pd.DataFrame({
        "source": [1, 2],
        "target": [2, 3]
    })
    G = build_connection_graph(df, "source", "target")
    for node in G.nodes:
        assert isinstance(node, str)