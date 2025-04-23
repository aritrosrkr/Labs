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

######## ALTERNATIVE ########
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