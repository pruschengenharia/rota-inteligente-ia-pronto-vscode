import time
from .search_algorithms import bfs_path, dfs_path, astar_path, path_cost

def evaluate_search(G, start, goal, metric="distance_km"):
    results = []
    for name, fn in [
        ("BFS", lambda: bfs_path(G, start, goal)),
        ("DFS", lambda: dfs_path(G, start, goal)),
        ("A*", lambda: astar_path(G, start, goal, metric)),
    ]:
        t0 = time.perf_counter()
        path = fn()
        t1 = time.perf_counter()
        cost = path_cost(G, path, metric) if path else float("inf")
        results.append(
            {
                "algorithm": name,
                "path": path,
                "cost": cost,
                "time_ms": (t1 - t0) * 1000,
                "nodes": len(path) if path else 0,
            }
        )
    return sorted(results, key=lambda r: (r["cost"], r["time_ms"]))
