class DisjointSet:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
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

    def parent_size(self, x):
        return self.size[self.find(x)]

N, K = map(int, input().split())
c = 0
cost = 0
dsu = DisjointSet(N)
edges = []
for _ in range(K):
    x, y, z = map(int, input().split())
    u = x - 1
    v = y - 1
    w = z
    edges.append((w, u, v))
edges.sort()

for w, u, v in edges:
    if dsu.find(u) == dsu.find(v):
        continue
    dsu.unite(u, v)
    cost += w
    c += 1
    if c == N-1:
        print(cost)