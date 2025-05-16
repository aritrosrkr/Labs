from collections import deque
 
class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
 
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
 
    def unite(self, x, y):
        x_par = self.find(x)
        y_par = self.find(y)
        if x_par == y_par:
            return
        if self.size[x_par] > self.size[y_par]:
            x_par, y_par = y_par, x_par
        self.parent[x_par] = y_par
        self.size[y_par] += self.size[x_par]
 
def find_max(G, u, d):
    visited = [False]*len(G)
    parent = [None]*len(G)
    max_edge = [0]*len(G)
    S = [(u, None, 0)]
 
    while S:
        cur, p, w = S.pop()
        if visited[cur]:
            continue
        visited[cur] = True
        parent[cur] = p
        max_edge[cur] = w
        for v, weight in G[cur]:
            if not visited[v]:
                S.append((v, cur, weight))
 
    cur = d
    max_w = 0
    while cur != u:
        if parent[cur] == None:
            return -1
        max_w = max(max_w, max_edge[cur])
        cur = parent[cur]
    return max_w
 
N, K = map(int, input().split())
graph = [[] for _ in range(N)]
edges = []
for _ in range(K):
    x, y, z = map(int, input().split())
    u = x - 1
    v = y - 1
    w = z
    edges.append([w, u, v, False])
edges.sort()
 
mst = DisjointSet(N)
c = 0
best = 0
for i in range(K):
    w, u, v, _ = edges[i]
    if mst.find(u) != mst.find(v):
        mst.unite(u, v)
        graph[u].append((v, w))
        graph[v].append((u, w))
        edges[i][3] = True
        best += w
        c += 1
        if c == N-1:
            break
        
if c != N-1:
    print(-1)
else:
    second_mst = float('inf')
    for w, u, v, in_mst in edges:
        if not in_mst:
            max_edge = find_max(graph, u, v)
            if max_edge != -1 and w != max_edge:
                second_mst = min(second_mst, best - max_edge + w)
                
    print(-1 if second_mst == float('inf') else second_mst)