from collections import deque

N, M = map(int, input().split())
graph = {k:[] for k in range(1, N+1)}
for _ in range(M):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

color = {k:None for k in graph}
visited = set()

def bipartite(G, s):
    visited.add(s)
    color[s] = 0
    count = [1, 0]
    Q = deque([s])
    while Q:
        u = Q.popleft()
        for v in G[u]:
            if v not in visited:
                visited.add(v)
                color[v] = 1 - color[u]
                count[color[v]] += 1
                Q.append(v)
    return max(count)

ans = 0
for v in range(1, N+1):
    if v not in visited:
        ans += bipartite(graph, v)

print(ans)