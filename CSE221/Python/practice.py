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

