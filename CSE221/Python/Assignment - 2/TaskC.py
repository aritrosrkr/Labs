N, K = tuple(map(int, input().split()))
arr = list(map(int, input().split()))
i = 0
j = 0

Max = 0
Sum = 0
while j < N:
    Sum += arr[j]
    while Sum > K and i < N:
        Sum -= arr[i]
        i += 1
    Max = max(Max, j - i + 1)
    j += 1

print(Max)    