N, M = map(int, input().split())
graph = [0]*N
n1 = tuple(map(int, input().split()))
n2 = tuple(map(int, input().split()))
for i in range(M):
    graph[n1[i]-1] -= 1
    graph[n2[i]-1] += 1
print(*graph)