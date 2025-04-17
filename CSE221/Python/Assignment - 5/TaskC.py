from collections import deque

N, M, S, D = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
n1 = tuple(map(int, input().split()))
n2 = tuple(map(int, input().split()))
for i in range(M):
    graph[n1[i]].append(n2[i])
    graph[n2[i]].append(n1[i])

for i in range(1, N+1):
    graph[i].sort()
    
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
        print(-1)
        return
    
    path = []
    cur = D
    while cur != None:
        path.append(cur)
        cur = prnt[cur]
    path.reverse()
    print(len(path)-1)
    print(*path)

shortest_path(graph, S, D)
