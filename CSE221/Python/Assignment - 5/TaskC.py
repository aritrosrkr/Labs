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

########### ALTERNATIVE ##########
from collections import deque

N, M, S, D = map(int, input().split())
n1 = list(map(int, input().split()))
n2 = list(map(int, input().split()))

graph = {k:[] for k in range(1, N+1)}
parent = {k:None for k in graph}
for i in range(M):
    graph[n1[i]].append(n2[i])
    graph[n2[i]].append(n1[i])

def shortest_path(G, s, d):
    visited = {k:False for k in G}
    visited[s] = True
    Q = deque([[s]])
    while Q:
        path = Q.popleft()
        u = path[-1]
        if u == d:
            print(len(path)-1)
            print(*path)
            return
        for v in sorted(G[u]):
            if not visited[v]:
                visited[v] = True
                new_path = list(path)
                new_path.append(v)
                Q.append(new_path)
        visited[u] = True
    print(-1)

shortest_path(graph, S, D)