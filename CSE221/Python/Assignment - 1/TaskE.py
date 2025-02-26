N = int(input())
n = input().split(' ')
arr = []

for i in n:
    arr += [int(i)]

for i in range(len(arr)-1):
    swapped = False
    for j in range(len(arr)-i-1): 
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]
            swapped = True
    if not swapped:
        break

print(*arr)