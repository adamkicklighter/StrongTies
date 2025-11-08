# test_data_loader.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pandas as pd
import pytest
from src.data_loader import is_safe_path, load_connections, load_all_connections

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
    csv_file.write_text(
        "First Name,Last Name,Company,Position\n"
        "Alice,Smith,Acme Inc,Engineer\n"
        "Bob,Jones,Acme Inc,Manager\n"
        "Alice,Smith,Acme Inc,Engineer"
    )
    df = load_connections(str(csv_file), "testuser", str(tmp_path))
    assert set(df.columns) == {"name", "company", "position", "user_id"}
    assert len(df) == 2  # duplicates dropped
    assert "alice smith" in df["name"].values
    assert all(df["user_id"] == "testuser")

def test_load_connections_invalid_path(tmp_path):
    csv_file = tmp_path.parent / "unsafe.csv"
    csv_file.write_text(
        "First Name,Last Name,Company,Position\n"
        "Charlie,Brown,Peanuts,Friend"
    )
    with pytest.raises(ValueError):
        load_connections(str(csv_file), "testuser", str(tmp_path))

def test_load_all_connections(tmp_path):
    csv1 = tmp_path / "alice_connections.csv"
    csv2 = tmp_path / "bob_connections.csv"
    csv1.write_text(
        "First Name,Last Name,Company,Position\n"
        "Alice,Smith,Acme Inc,Engineer\n"
        "Bob,Jones,Acme Inc,Manager"
    )
    csv2.write_text(
        "First Name,Last Name,Company,Position\n"
        "Bob,Jones,Acme Inc,Manager\n"
        "Carol,White,Acme Inc,Designer"
    )
    df = load_all_connections(str(tmp_path))
    assert set(df.columns) == {"name", "company", "position", "user_id"}
    assert len(df) == 3  # Bob is duplicate
    assert sorted(df["name"].values) == ["alice smith", "bob jones", "carol white"]
    assert set(df["user_id"].values) == {"alice", "bob"}

def test_load_all_connections_empty(tmp_path):
    df = load_all_connections(str(tmp_path))
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_load_connections_hash_and_obfuscate(tmp_path, monkeypatch):
    # Mock sanitize_csv to check that hash_ids and obfuscate_names are passed
    called = {}
    def mock_sanitize_csv(df, hash_ids=False, obfuscate_names=False):
        called['hash_ids'] = hash_ids
        called['obfuscate_names'] = obfuscate_names
        return df
    monkeypatch.setattr("src.data_loader.sanitize_csv", mock_sanitize_csv)
    csv_file = tmp_path / "connections.csv"
    csv_file.write_text(
        "First Name,Last Name,Company,Position\n"
        "Alice,Smith,Acme Inc,Engineer"
    )
    load_connections(str(csv_file), "testuser", str(tmp_path), hash_ids=True, obfuscate_names=True)
    assert called['hash_ids'] is True
    assert called['obfuscate_names'] is True

def test_load_connections_standardization(tmp_path, monkeypatch):
    # Mock company and position cleaners
    monkeypatch.setattr("src.data_loader.clean_company_name", lambda x: "StandardCo")
    monkeypatch.setattr("src.data_loader.standardize_position_title", lambda x: "StandardTitle")
    csv_file = tmp_path / "connections.csv"
    csv_file.write_text(
        "First Name,Last Name,Company,Position\n"
        "Alice,Smith,Acme Inc,Engineer"
    )
    df = load_connections(str(csv_file), "testuser", str(tmp_path))
    assert df["company"].iloc[0] == "StandardCo"
    assert df["position"].iloc[0] == "StandardTitle"

def test_load_connections_malformed_csv(tmp_path):
    # Missing required columns
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(
        "First Name,Company\n"
        "Alice,Acme Inc"
    )
    with pytest.raises(ValueError):
        load_connections(str(csv_file), "testuser", str(tmp_path))

def test_load_all_connections_ignores_non_csv(tmp_path):
    csv_file = tmp_path / "alice_connections.csv"
    txt_file = tmp_path / "bob_connections.txt"
    csv_file.write_text(
        "First Name,Last Name,Company,Position\n"
        "Alice,Smith,Acme Inc,Engineer"
    )
    txt_file.write_text("Not a CSV")
    df = load_all_connections(str(tmp_path))
    assert "alice smith" in df["name"].values
    assert "bob_connections.txt" not in df["name"].values

def test_load_connections_logging(tmp_path, caplog):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text(
        "First Name,Company\n"
        "Alice,Acme Inc"
    )
    with caplog.at_level("ERROR"):
        with pytest.raises(ValueError):
            load_connections(str(csv_file), "testuser", str(tmp_path))
        assert any("CSV missing required columns" in m for m in caplog.messages)