import sys
sys.setrecursionlimit(2*100000+10)
 
N, M = map(int, input().split())
 
graph = {k:[] for k in range(1, N+1)}
visited = {k: False for k in range(1, N+1)}
in_stack = {k: False for k in range(1, N+1)}
cycle = False
 
for i in range(M):
    u, v = map(int, input().split())
    graph[u].append(v)
 
def find_cycle(G, u):
    visited[u] = True
    in_stack[u] = True
    for v in G[u]:
        if not visited[v]:
            if find_cycle(G, v) == 'YES':
                return 'YES'
        elif in_stack[v]:
            return 'YES'
        
    in_stack[u] = False
    return 'NO'
 
for i in range(1, N+1):
    if not visited[i]:
        if find_cycle(graph, i) == 'YES':
            cycle = True
            break
 
if cycle:
    print('YES')
else:
    print('NO')