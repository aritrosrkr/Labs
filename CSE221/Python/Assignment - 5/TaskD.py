from collections import deque

N, M, S, D, K = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
for i in range(M):
    u, v = map(int, input().split())
    graph[u].append(v)
    
def shortest_path(G, S, D):
    traversal = []
    color = {k: 'WHITE' for k in graph}
    prnt = {k:  None for k in graph}

    Q = deque([S])
    color[S] = 'GREY'
    while Q:
        u = Q.popleft()
        traversal.append(u)
        for v in G[u]:
            if color[v] == 'WHITE':
                color[v] = 'GREY'
                prnt[v] = u
                Q.append(v)
        color[u] = 'BLACK'
    
    if prnt[D] == None and S != D:
        return None
    
    path = []
    cur = D
    while cur != None:
        path.append(cur)
        cur = prnt[cur]
    path.reverse()
    return path

p1 = shortest_path(graph, S, K)
p2 = shortest_path(graph, K, D)

if p1 == None or p2 == None:
    print(-1)
else:
    path = p1 + p2[1:]
    print(len(path)-1)
    print(*path)