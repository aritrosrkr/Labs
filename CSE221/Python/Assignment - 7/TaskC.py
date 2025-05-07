import heapq

N, M = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
weight = {}
for _ in range(M):
    u, v, w = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)
    weight[(u, v)] = w
    weight[(v, u)] = w
    
def dijkstra(G, s):
    Q = [(0, s)]
    danger = {k:float('inf') for k in graph}
    danger[s] = 0
    while Q:
        danger_u, u = heapq.heappop(Q)
        if danger_u > danger[u]:
            continue
        for v in G[u]:
            if max(danger_u, weight[(u, v)]) < danger[v]:
                danger[v] = max(danger_u, weight[(u, v)])
                heapq.heappush(Q, (danger[v], v))
    danger[1] = 0
    return danger

danger = dijkstra(graph, 1)
for v in danger.values():
    if v == float('inf'):
        print(-1, end = ' ')
    else:
        print(v, end = ' ')