N, M = map(int, input().split())
graph = [0]*N
n1 = tuple(map(int, input().split()))
n2 = tuple(map(int, input().split()))
odd = 0
for i in range(M):
    graph[n1[i]-1] += 1
    graph[n2[i]-1] += 1
for i in graph:
    if i%2 != 0:
        odd += 1
if odd == 0 or odd == 2:
    print("YES")
else:
    print("NO")