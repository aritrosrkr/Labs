import heapq

N, M, S, D = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
distance = {k:float('inf') for k in graph}
parent = {k:-1 for k in graph}
weights = {}
for _ in range(M):
    u, v, w = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)
    weights[(u, v)] = w
    weights[(v, u)] = w

def second_dijkstra(G, s, d):
    Q = [(0, s)]
    dist1 = {k:float('inf') for k in graph}
    dist2 = {k:float('inf') for k in graph}
    dist1[s] = 0
    while Q:
        dist_u, u = heapq.heappop(Q)
        for v in G[u]:
            if dist_u + weights[(u, v)] < dist1[v]:
                dist2[v] = dist1[v]
                dist1[v] = dist_u + weights[(u, v)]
                heapq.heappush(Q, (dist1[v], v))
            elif dist1[v] < dist_u + weights[(u, v)] < dist2[v]:
                dist2[v] = dist_u + weights[(u, v)]
                heapq.heappush(Q, (dist2[v], v))
    
    if dist2[d] == float('inf'):
        return -1
    return dist2[d]

print(second_dijkstra(graph, S, D))