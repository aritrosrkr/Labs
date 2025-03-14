N = int(input())
arr = list(map(int, input().split()))

l = 0
r = len(arr) - 1

def max_sum(arr, l, r):
    if l >= r:
        return -1
    
    m = (l + r)//2
    L = max_sum(arr, l, m)
    R = max_sum(arr, m + 1, r)

    L_max = max(arr[l:m+1])
    R_max = max(arr[m+1:r+1])
    R_min= min(arr[m+1:r+1])

    C_max = max(L_max + R_max**2, L_max + R_min**2)
    return max(L, C_max, R)

print(max_sum(arr, l, r))