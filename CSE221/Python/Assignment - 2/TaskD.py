T = int(input())
for i in range(T):
    S = input()
    found = False
    upper = len(S)
    lower = 0
    while lower < upper:
        mid = (upper + lower) // 2
        if S[mid] == '0':
            lower = mid + 1
        elif S[mid] == '1':
            if mid - 1 < 0 or S[mid-1] == '0':
                print(mid+1)
                found = True
                break
            else:
                upper = mid

    if not found:
        print(-1)