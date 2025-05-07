import heapq

N, M, S, D = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
weights = list(map(int, input().split()))
for _ in range(M):
    u, v = map(int, input().split())
    graph[u].append(v)

def dijkstra(G, s, d):
    distance = {k:float('inf') for k in G}
    distance[s] = weights[s-1]
    Q = [(distance[s], s)]
    while Q:
        dist_u, u = heapq.heappop(Q)
        if dist_u > distance[u]:
            continue
        if u == d:
            if distance[u] == float('inf'):
                return -1
            return distance[u]
        for v in G[u]:
            if dist_u + weights[v-1] < distance[v]:
                distance[v] = dist_u + weights[v-1]
                heapq.heappush(Q, (distance[v], v))
    return -1

print(dijkstra(graph, S, D))