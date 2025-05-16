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
friendship = DisjointSet(N)
for _ in range(K):
    x, y = map(int, input().split())
    a = x - 1
    b = y - 1
    friendship.unite(a, b)
    print(friendship.parent_size(a))