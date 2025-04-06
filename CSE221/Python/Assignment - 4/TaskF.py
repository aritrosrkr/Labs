N = int(input())
pos = tuple(map(int, input().split()))
ans = []
moves = [(-1,-1), (-1, 0), (-1,1), (0,-1), (0,1), (1,-1), (1, 0), (1,1)]
for i, j in moves:
    x = pos[0] + i
    y = pos[1] + j
    if 1 <= x <= N and 1 <= y <= N:
        ans.append((x,y))

print(len(ans))
for x in ans:
    print(*x)