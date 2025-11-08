import sys
import os
import argparse
import networkx as nx

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_all_connections
from src.graph_builder import build_connection_graph

def main(data_dir, output_path):
    df = load_all_connections(data_dir)
    G = build_connection_graph(df, source_col="user_id", target_col="name")
    print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

    # Ensure the results directory exists
    results_dir = os.path.dirname(output_path)
    if results_dir and not os.path.exists(results_dir):
        os.makedirs(results_dir, exist_ok=True)

    nx.write_graphml(G, output_path)
    print(f"Graph saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Construct and save a professional social graph.")
    parser.add_argument("--data_dir", type=str, default="data", help="Directory with connection CSVs")
    parser.add_argument("--output", type=str, default="results/figures/network.graphml", help="Output graph file")
    args = parser.parse_args()
    main(args.data_dir, args.output)