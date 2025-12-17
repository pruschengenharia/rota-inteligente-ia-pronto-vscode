import argparse
import os
import matplotlib.pyplot as plt

from .graph_loader import load_graph
from .plot_graph import plot_graph, export_graphviz_dot
from .evaluate import evaluate_search
from .clustering import load_deliveries, run_kmeans

def plot_clusters(df, centroids, out="docs/kmeans_clusters.png"):
    os.makedirs("docs", exist_ok=True)
    plt.figure(figsize=(10, 7))
    for c in sorted(df["cluster"].unique()):
        subset = df[df["cluster"] == c]
        plt.scatter(subset["x"], subset["y"], s=200, label=f"Cluster {c}", alpha=0.7)

    plt.scatter(
        centroids[:, 0],
        centroids[:, 1],
        marker="X",
        s=400,
        c="red",
        edgecolors="black",
        linewidths=2,
        label="Centroides",
    )

    for _, row in df.iterrows():
        plt.annotate(
            str(row["delivery_id"]),
            (row["x"], row["y"]),
            fontsize=10,
            fontweight="bold",
            ha="center",
            va="center",
        )

    plt.title("K-Means - Agrupamento", fontsize=16, fontweight="bold")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✓ Clusters: {out}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--nodes", default="data/nodes.csv")
    p.add_argument("--edges", default="data/edges.csv")
    p.add_argument("--deliveries", default="data/deliveries.csv")
    p.add_argument("--start", default="A")
    p.add_argument("--goal", default="F")
    p.add_argument("--metric", default="distance_km", choices=["distance_km", "time_min"])
    p.add_argument("--k", type=int, default=2)
    args = p.parse_args()

    print("\n" + "=" * 60)
    print("🚀 ROTA INTELIGENTE - OTIMIZAÇÃO COM IA")
    print("=" * 60 + "\n")

    print("[1/4] Carregando grafo...")
    G = load_graph(args.nodes, args.edges)
    print(f"      ✓ {G.number_of_nodes()} nós, {G.number_of_edges()} arestas\n")

    print("[2/4] Gerando visualizações...")
    plot_graph(G)
    export_graphviz_dot(G)

    print("\n[3/4] Comparando algoritmos...")
    print(f"      {args.start} → {args.goal}\n")
    results = evaluate_search(G, args.start, args.goal, args.metric)

    print("      " + "-" * 55)
    print(f"      {'Algo':<8} {'Caminho':<20} {'Custo':<10} {'Tempo(ms)'}")
    print("      " + "-" * 55)
    for r in results:
        path_str = " → ".join(r["path"]) if r["path"] else "N/A"
        print(f"      {r['algorithm']:<8} {path_str:<20} {r['cost']:<10.2f} {r['time_ms']:.3f}")
    print("      " + "-" * 55)

    print("\n[4/4] Executando K-Means...")
    df = load_deliveries(args.deliveries)
    clustered, cents, inertia = run_kmeans(df, args.k)
    plot_clusters(clustered, cents)

    print(f"\n      K={args.k}, Inércia={inertia:.2f}")
    for c in sorted(clustered["cluster"].unique()):
        ids = ", ".join(map(str, clustered[clustered["cluster"] == c]["delivery_id"]))
        print(f"      • Cluster {c}: {ids}")

    print("\n" + "=" * 60)
    print("✅ CONCLUÍDO! Veja docs/")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
