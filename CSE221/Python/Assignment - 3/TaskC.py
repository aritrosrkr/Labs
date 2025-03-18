a, b = map(int, input().split())
if a % 107 == 0:
    print(0)
else:
    ans = 1
    while b > 0:
        if b % 2 != 0:
            ans = (a * ans) % 107
        b = b // 2
        a = (a * a) % 107
print(ans)