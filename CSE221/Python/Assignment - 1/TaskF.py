N = int(input())
id = input().split(' ')
mark = input().split(' ')
swaps = 0

ids = []
marks = []

for i in range(N):
    ids += [int(id[i])]
    marks += [int(mark[i])]

for i in range(N-1):
    ind = i
    for j in range(i+1, N):
        if i != j:
            if marks[ind] < marks[j]:
                ind = j
            elif marks[ind] == marks[j]:
                if ids[ind] > ids[j]:
                    ind = j
    if ind != i:
        marks[ind], marks[i] = marks[i], marks[ind]
        ids[ind], ids[i] = ids[i], ids[ind]
        swaps += 1

print(f"Minimum swaps: {swaps}")
for i in range(N):
    print(f"ID: {ids[i]} Mark: {marks[i]}")
