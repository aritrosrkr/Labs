N, M = map(int, input().split())
mat = [['0']*N for _ in range(N)]
for _ in range(M):
    x = tuple(map(int, input().split()))
    mat[x[0]-1][x[1]-1] = str(x[2])
for row in mat:
    print(" ".join(row))
    