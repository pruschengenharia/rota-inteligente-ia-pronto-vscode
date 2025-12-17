import pandas as pd
import networkx as nx

def load_graph(nodes_path, edges_path):
    """Carrega grafo dos CSVs"""
    nodes_df = pd.read_csv(nodes_path)
    edges_df = pd.read_csv(edges_path)
    G = nx.Graph()

    for _, row in nodes_df.iterrows():
        G.add_node(
            row["id"],
            label=row["label"],
            type=row["type"],
            x=float(row["x"]),
            y=float(row["y"]),
        )

    for _, row in edges_df.iterrows():
        G.add_edge(
            row["source"],
            row["target"],
            distance_km=float(row["distance_km"]),
            time_min=float(row["time_min"]),
        )
    return G
