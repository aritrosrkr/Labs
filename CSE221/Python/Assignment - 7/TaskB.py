import heapq

N, M, S, T = map(int, input().split())
graph = {k:[] for k in range(1, N+1)}
parent = {k:-1 for k in graph}
weight = {}
for _ in range(M):
    u, v, w = map(int, input().split())
    graph[u].append(v)
    weight[(u, v)] = w

def dijkstra(G, s):
    Q = [(0, s)]
    distance = {k:float('inf') for k in graph}
    distance[s] = 0
    while Q:
        dist_u, u = heapq.heappop(Q)
        for v in G[u]:
            if dist_u + weight[(u, v)] < distance[v]:
                distance[v] = distance[u] + weight[(u, v)]
                parent[v] = u
                heapq.heappush(Q, (distance[v], v))
    return distance

Alice = dijkstra(graph, S)
Bob = dijkstra(graph, T)
best = [float('inf'), None]
for i in range(1, N+1):
    if Alice[i] != float('inf') and Bob[i] != float('inf'):
        min_time = max(Alice[i], Bob[i])
        if min_time < best[0]:
            best[0] = min_time
            best[1] = i
        elif min_time == best[0] and i < best[1]:
            best[1] = i
        
if best != [float('inf'), None]:
    print(best[0], best[1])
else:
    print(-1)