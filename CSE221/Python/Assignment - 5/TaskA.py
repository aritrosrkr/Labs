N, M = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
for i in range(M):
    n1, n2 = tuple(map(int, input().split()))
    graph[n1].append(n2)
    graph[n2].append(n1)

def bfs(G, s):
    traversal = []
    color = {k: 'WHITE' for k in graph}
    
    Q = [s]
    color[s] = 'GREY'
    while Q:
        u = Q.pop(0)
        traversal.append(u)
        for v in G[u]:
            if color[v] == 'WHITE':
                color[v] = 'GREY'
                Q.append(v)
        color[u] = 'BLACK'
    return traversal

print(*bfs(graph, 1))