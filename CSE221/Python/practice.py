t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    x = []
    c = 1
    if all(x != -1 for x in b):
        for i in range(n):
            if b[i] != -1:
                if x <= k:
                    x = a[i] + b[i]
                    break
        for i in range(n):
            if b[i] == -1:
                b[i] = x - a[i]
        for i in range(n):
            if a[i] + b[i] != x:
                c = 0
                break

    else:
        for i in range(n):
            x = a[i] + b[i]
            if a[i] <= x <= a[i] + k:
                c += 1
    
    print(c)
            