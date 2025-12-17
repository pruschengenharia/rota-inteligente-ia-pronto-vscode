from collections import deque
import heapq
import math

def bfs_path(G, start, goal):
    queue = deque([start])
    visited, parent = {start}, {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            return _reconstruct(parent, goal)
        for n in G.neighbors(node):
            if n not in visited:
                visited.add(n)
                parent[n] = node
                queue.append(n)
    return None

def dfs_path(G, start, goal):
    stack, visited, parent = [start], {start}, {start: None}
    while stack:
        node = stack.pop()
        if node == goal:
            return _reconstruct(parent, goal)
        for n in G.neighbors(node):
            if n not in visited:
                visited.add(n)
                parent[n] = node
                stack.append(n)
    return None

def astar_path(G, start, goal, metric="distance_km"):
    def h(n):
        x1, y1 = G.nodes[n]["x"], G.nodes[n]["y"]
        x2, y2 = G.nodes[goal]["x"], G.nodes[goal]["y"]
        return math.dist((x1, y1), (x2, y2))

    heap = [(0, start)]
    g_cost, parent, closed = {start: 0}, {start: None}, set()

    while heap:
        _, cur = heapq.heappop(heap)
        if cur == goal:
            return _reconstruct(parent, goal)
        if cur in closed:
            continue
        closed.add(cur)

        for n in G.neighbors(cur):
            w = G[cur][n].get(metric, 1)
            tent = g_cost[cur] + w
            if tent < g_cost.get(n, float("inf")):
                g_cost[n] = tent
                parent[n] = cur
                heapq.heappush(heap, (tent + h(n), n))
    return None

def path_cost(G, path, metric="distance_km"):
    if not path or len(path) < 2:
        return 0
    return sum(G[path[i]][path[i + 1]][metric] for i in range(len(path) - 1))

def _reconstruct(parent, goal):
    path = []
    while goal:
        path.append(goal)
        goal = parent.get(goal)
    return path[::-1]
