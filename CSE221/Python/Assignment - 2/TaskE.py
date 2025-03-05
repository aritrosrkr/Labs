n, q = (map(int, input().split()))
arr = list(map(int, input().split()))
for i in range(q):
    l = -1
    r = -1
    
    x, y = map(int, input().split())
    x_upper = len(arr) - 1
    x_lower = 0
    while x_lower <= x_upper:
        mid = (x_upper + x_lower)//2
        if arr[mid] >= x:
            l = mid
            x_upper = mid - 1
        else:
            x_lower = mid + 1

    y_upper = len(arr) - 1
    y_lower = 0
    while y_lower <= y_upper:
        mid = (y_upper + y_lower)//2
        if arr[mid] <= y:
            r = mid
            y_lower = mid + 1
        else:
            y_upper = mid - 1
            
    if l != -1 and r!= -1:
        print(r - l + 1)
    else:
        print(0)