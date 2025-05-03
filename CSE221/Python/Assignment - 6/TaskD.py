N, R = map(int, input().split())
graph = {k:[] for k in range(1, N+1)}
for _ in range(N-1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

Q = int(input())
size = {k:0 for k in graph}
parent = {k:None for k in graph}
traversal = []

def dfs(G, s):
    visited = {k:False for k in graph}
    processed = {k:False for k in graph}
    S = [s]
    while S:
        u = S.pop()
        if processed[u]:
            traversal.append(u)
        elif not visited[u]:
            visited[u] = True
            S.append(u)
            for v in G[u]:
                if not visited[v]:
                    S.append(v)
            processed[u] = True 

def subtree_length(u):
    dfs(graph, u)
    for u in traversal:
        size[u] = 1
        for v in graph[u]:
            if v != parent[u]:
                size[u] += size[v]

subtree_length(R)
for _ in range(Q):
    v = int(input())
    print(size[v])