import os
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G, out="docs/grafo.png"):
    os.makedirs("docs", exist_ok=True)
    pos = {n: (G.nodes[n]["x"], G.nodes[n]["y"]) for n in G.nodes}

    colors = []
    for n in G.nodes:
        t = G.nodes[n].get("type")
        colors.append("#ef4444" if t == "warehouse" else "#10b981" if t == "home" else "#3b82f6")

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=colors, edgecolors="white", linewidths=3)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    labels = {(u, v): f'{d["distance_km"]} km' for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, labels, font_size=9)

    plt.title("Grafo da Cidade - Sabor Express", fontsize=16, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✓ Grafo: {out}")

def export_graphviz_dot(G, out="docs/grafo.dot"):
    try:
        nx.drawing.nx_pydot.write_dot(G, out)
        print(f"✓ DOT: {out}")
    except Exception:
        pass
