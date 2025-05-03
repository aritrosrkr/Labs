from collections import deque

N = int(input())
graph = {k:[] for k in range(1, N+1)}
for _ in range(N-1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

visited = {k:False for k in graph}
parent = {k:None for k in graph}
dist = {k:0 for k in graph}
def bfs(G, s):
    visited[s] = True
    dist[s] = 0
    d = s
    Q = deque([s])
    while Q:
        u = Q.popleft()
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                dist[v] = dist[u] + 1
                parent[v] = u
                Q.append(v)
                if dist[v] > dist[d]:
                    d = v
        visited[u] = True
    return d

A = bfs(graph, 1)

visited = {k:False for k in graph}
parent = {k:None for k in graph}
dist = {k:0 for k in graph}
B = bfs(graph, A)

p = []
cur = B
while cur != None:
    p.append(cur)
    cur = parent[cur]

print(f"{len(p)-1}\n{p[0]} {p[-1]}")
