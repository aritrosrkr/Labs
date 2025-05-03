import heapq

N = int(input())
graph = {}
in_degree = {}
words = []
chars = set()
for _ in range(N):
    S = input()
    words.append(S)

for word in words:
    for ch in word:
        chars.add(ch)

for ch in chars:
    graph[ch] = []
    in_degree[ch] = 0

def kahn_sort(G):
    Q = []
    ans = []
    for v in G:
        if in_degree[v] == 0:
            heapq.heappush(Q, v)
    while Q:
        u = heapq.heappop(Q)
        ans.append(u)
        for v in G[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(Q, v)

    if len(ans) == len(G):
        print(''.join(ans))
    else:
        print(-1)

valid = True
for i in range(1, N):
    w2 = words[i]
    w1 = words[i-1]
    found = False
    for j in range(min(len(w1), len(w2))):
        if w1[j] != w2[j]:
            graph[w1[j]].append(w2[j])
            in_degree[w2[j]] += 1
            found = True
            break
    if not found and len(w1) > len(w2):
        valid = False

if valid:
    kahn_sort(graph)
else:
    print(-1)