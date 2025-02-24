T = input().split(' ')
n = int(T[0])
k = int(T[1])
arr = input().split(' ')
arr = arr[:k:]
temp = [0]*k
for i in range(1, k+1):
    temp[-i] = arr[i-1]
print(' '.join(temp))
