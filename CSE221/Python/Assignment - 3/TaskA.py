N = int(input())
arr0 = list(map(int, input().split()))

c = 0
def merge(a, b):
    i = 0
    j = 0
    new = []
    global c
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            new.append(a[i])
            i += 1
        else:
            new.append(b[j])
            c += len(a) - i
            j += 1
    new += a[i::]
    new += b[j::]
    return new

def mergeSort(arr):
    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr)//2
        a1 = mergeSort(arr[:mid:])
        a2 = mergeSort(arr[mid::])
        return merge(a1, a2)

arr1 = (mergeSort(arr0))
print(c)
print(*arr1)

