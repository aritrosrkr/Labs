import sys
sys.setrecursionlimit(2*100000)

N, M = map(int, input().split())

graph = {k:[] for k in range(1, N+1)}
n1 = tuple(map(int, input().split()))
n2 = tuple(map(int, input().split()))
for i in range(M):
    graph[n1[i]].append(n2[i])
    graph[n2[i]].append(n1[i])
    
traversal = []
color = {k:'WHITE' for k in graph}
def dfs_visit(u):
    global graph
    traversal.append(u)
    color[u] = 'GREY'
    for v in graph[u]:
        if color[v] == 'WHITE':
            dfs_visit(v)
    color[u] = 'BLACK'

def dfs(G):
    for u in G:
        if color[u] == 'WHITE':
            dfs_visit(u)
    return traversal

print(*dfs(graph))