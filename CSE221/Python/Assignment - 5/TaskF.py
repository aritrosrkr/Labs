from collections import deque

R, H = map(int, input().split())
graph = [list(input()) for i in range(R)]
visited = [[False]*H for i in range(R)]
            
def bfs(s):
    points = 0
    visited[s[0]][s[1]] = True
    
    Q = deque([s])
    while Q:
        r, h = Q.popleft()
        if graph[r][h] == 'D':
            points += 1
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            i, j = r + x, h + y
            if 0 <= i < R and 0 <= j < H and graph[i][j] != '#' and visited[i][j] == False:
                visited[i][j] = True
                Q.append((i, j))
    return points

points = 0
for i in range(R):
    for j in range(H):
        if graph[i][j] != '#' and visited[i][j] == False:
            points = max(points, bfs((i, j)))
            
print(points)