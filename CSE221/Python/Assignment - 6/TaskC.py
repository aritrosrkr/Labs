from collections import deque

N = int(input())
x0, y0, x1, y1 = map(int, input().split())
visited = [[-1]*N for _ in range(N)]
def bfs(s):
    directions = [(1,2), (2,1), (-1,2), (-2,1), (1,-2), (2,-1), (-1,-2), (-2,-1)]
    Q = deque([(s[0], s[1], 0)])
    visited[s[0]-1][s[1]-1] = 0
    while Q:
        x0, y0, m = Q.popleft()
        for x, y in directions:
            a, b = x + x0, y + y0
            if (a,b) == (x1,y1):
                return m+1
            if 1 <= a <= N and 1 <= b <= N and visited[a-1][b-1] == -1:
                visited[a-1][b-1] = 0
                Q.append((a,b,m+1))
    return -1

print(bfs((x0,y0)))