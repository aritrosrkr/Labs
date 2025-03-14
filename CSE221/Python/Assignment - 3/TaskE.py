N = int(input())
arr = list(map(int, input().split()))

l = 0
r = len(arr) - 1

def balanceBST(arr, l, r):
    if l > r:
        return []
    
    m = (l + r)//2
    root = arr[m]
    
    left = balanceBST(arr, l, m-1)
    right = balanceBST(arr, m+1, r)
    return [root] + left + right

print(*balanceBST(arr, l, r))