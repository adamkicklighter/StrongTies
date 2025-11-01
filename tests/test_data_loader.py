# test_data_loader.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import os
import pandas as pd
import pytest
from data_loader import is_safe_path, load_connections, load_all_connections

def test_is_safe_path(tmp_path):
    base_dir = tmp_path
    safe_file = base_dir / "safe.csv"
    safe_file.write_text("header\nvalue")
    unsafe_file = tmp_path.parent / "unsafe.csv"
    unsafe_file.write_text("header\nvalue")
    assert is_safe_path(str(base_dir), str(safe_file)) is True
    assert is_safe_path(str(base_dir), str(unsafe_file)) is False

def test_load_connections_valid(tmp_path):
    csv_file = tmp_path / "connections.csv"
    csv_file.write_text("Name, Email\nAlice, alice@example.com\nBob, bob@example.com\nAlice, alice@example.com")
    df = load_connections(str(csv_file), str(tmp_path))
    assert set(df.columns) == {"name", "email"}
    assert len(df) == 2  # duplicates dropped
    assert "alice@example.com" in df["email"].values

def test_load_connections_invalid_path(tmp_path):
    csv_file = tmp_path.parent / "unsafe.csv"
    csv_file.write_text("Name, Email\nCharlie, charlie@example.com")
    with pytest.raises(ValueError):
        load_connections(str(csv_file), str(tmp_path))

def test_load_all_connections(tmp_path):
    csv1 = tmp_path / "a.csv"
    csv2 = tmp_path / "b.csv"
    csv1.write_text("Name, Email\nAlice, alice@example.com\nBob, bob@example.com")
    csv2.write_text("Name, Email\nBob, bob@example.com\nCarol, carol@example.com")
    df = load_all_connections(str(tmp_path))
    assert set(df.columns) == {"name", "email"}
    assert len(df) == 3  # Bob is duplicate
    assert sorted(df["name"].values) == ["Alice", "Bob", "Carol"]

def test_load_all_connections_empty(tmp_path):
    df = load_all_connections(str(tmp_path))
    assert isinstance(df, pd.DataFrame)
    assert df.empty