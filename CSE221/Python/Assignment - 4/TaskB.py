N, M = map(int, input().split())
graph = [[] for i in range(N)]
n1 = tuple(map(int, input().split()))
n2 = tuple(map(int, input().split()))
wt = tuple(map(int, input().split()))
for i in range(M):
    graph[n1[i]-1].append((n2[i], wt[i]))
for i in range(N):
    print(f"{i+1}:", *graph[i])