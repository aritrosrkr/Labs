import heapq

N, M = map(int, input().split())
n1 = list(map(int, input().split()))
n2 = list(map(int, input().split()))
w = list(map(int, input().split()))

graph = {k:[] for k in range(1, N+1)}
distance = {k:float('inf') for k in graph}
parent = {k:-1 for k in graph}
weights = {}
for i in range(M):
    graph[n1[i]].append(n2[i])
    weights[(n1[i], n2[i])] = w[i]
    
def dijkstra(G, s):
    Q = []
    distance = {k:[float('inf'), float('inf')] for k in G}
    for v in G[s]:
        parity = weights[(s,v)] % 2
        distance[v][parity] = weights[(s,v)]
        heapq.heappush(Q, (weights[(s,v)], v, parity))
        
    while Q:
        dist_u, u, prev = heapq.heappop(Q)
        if dist_u > distance[u][prev]:
            continue
        for v in G[u]:
            cur = weights[(u,v)] % 2
            if cur != prev and dist_u + weights[(u,v)] < distance[v][cur]:
                distance[v][cur] = dist_u + weights[(u,v)]
                heapq.heappush(Q, (distance[v][cur], v, cur))

    ans = min(distance[N])
    if ans == float('inf'):
        return -1
    return ans

print(dijkstra(graph, 1))