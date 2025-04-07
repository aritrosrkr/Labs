N = int(input())
pos = tuple(map(int, input().split()))

# ans = []
# moves = [(-1,-1), (-1, 0), (-1,1), (0,-1), (0,1), (1,-1), (1, 0), (1,1)]
# for i, j in moves:
#     x = pos[0] + i
#     y = pos[1] + j
#     if 1 <= x <= N and 1 <= y <= N:
#         ans.append((x,y))

# print(len(ans))
# for x in ans:
#     print(*x)

moves = []
def check(x,y):
    global moves
    if 1<=x<=N and 1<=y<=N and (x,y) not in moves:
        moves.append((x,y))

x = pos[0]
y = pos[1]
check(x-1, y-1)
check(x-1, y)
check(x-1, y+1)
check(x, y-1)
check(x, y+1)
check(x+1, y-1)
check(x+1, y)
check(x+1, y+1)

print(len(moves))
for x in moves:
    print(*x)