N = int(input())
mat = [[0]*N for i in range(N)]
for i in range(N):
    x = tuple(map(int, input().split()))
    for ind in range(1, len(x)):
        mat[i][x[ind]] = 1
for row in mat:
    print(*row)