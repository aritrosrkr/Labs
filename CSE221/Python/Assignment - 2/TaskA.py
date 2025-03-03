N, S = tuple(map(int, input().split()))
arr = list(map(int, input().split()))
sum = 0
i = 0
j = len(arr) - 1
found = False
while i < j:
    sum = arr[i] + arr[j]
    if sum < S:
        i += 1
    elif sum > S:
        j -= 1
    else:
        found = True
        print(i+1, j+1)
        break
if not found:
    print(-1)