import heapq

N, M = map(int, input().split())
graph = {k:[] for k in range(1, N+1)}
in_degree = {k:0 for k in graph}
for _ in range(M):
    u, v = map(int, input().split())
    graph[u].append(v)
    in_degree[v] += 1
    
def kahn_sort(G):
    ans = []
    Q = []
    for v in G:
        if in_degree[v] == 0:
            heapq.heappush(Q, -v)

    while Q:
        u = -heapq.heappop(Q)
        ans.append(u)
        for v in G[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(Q, -v)
    
    if len(ans) == N:
        print(*ans)
    else:
        print(-1)

kahn_sort(graph)