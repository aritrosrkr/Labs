import heapq

N, M, S, D = map(int, input().split())
n1 = list(map(int, input().split()))
n2 = list(map(int, input().split()))
w = list(map(int, input().split()))

graph = {k:[] for k in range(1, N+1)}
distance = {k:float('inf') for k in graph}
parent = {k:-1 for k in graph}
weight = {}
for i in range(M):
    graph[n1[i]].append(n2[i])
    weight[(n1[i], n2[i])] = w[i]

def dijkstra(G, s, d):
    Q = [(0, s)]
    distance[s] = 0
    while Q:
        dist_u, u = heapq.heappop(Q)
        if u == d:
            return True
        for v in G[u]:
            if dist_u + weight[(u, v)] < distance[v]:
                distance[v] = distance[u] + weight[(u, v)]
                parent[v] = u
                heapq.heappush(Q, (distance[v], v))
    return False

if dijkstra(graph, S, D):
    path = []
    cur = D
    while cur != -1 and cur != S:
        path.append(cur)
        cur = parent[cur]
    path.append(S)
    path.reverse()
    print(distance[D])
    print(*path)
else:
    print(-1)