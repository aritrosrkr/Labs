import math
N, Q = map(int, input().split())
graph = []
for i in range(1, N+1):
    ans = []
    for j in range(1, N+1):
        if i != j and math.gcd(i,j) == 1:
            ans.append(j)
    graph.append(ans)
    ans = []
    
for _ in range(Q):
    X, K = map(int, input().split())
    if len(graph[X-1]) > K-1:
        print(graph[X-1][K-1])
    else:
        print(-1)