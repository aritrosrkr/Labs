N = int(input())
arrN = list(map(int, input().split()))
M = int(input())
arrM = list(map(int, input().split()))

arr = []
i = 0
j = 0
while i < N and j < M:
    if arrN[i] <= arrM[j]:
        arr.append(arrN[i])
        i += 1
    elif arrN[i] > arrM[j]:
        arr.append(arrM[j])
        j += 1
        
arr += arrN[i::]
arr += arrM[j::]
print(*arr)
    
    