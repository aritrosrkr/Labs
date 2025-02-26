N = int(input())
trains = []
names = []
times = []

for i in range(N):
    x = input()
    trains += [x]
    
for train in trains:
    train = train.split(' ')
    names += [train[0]]
    times += [train[-1]]

# for i in range(N-1):
#     ind = i
#     for j in range(i+1, N):
#         if i != j:
#             if names[ind] > names[j]:
#                 ind = j
#             elif names[ind] == names[j]:
#                 if times[ind] < times[j]:
#                     ind = j
#     if ind != i:
#         trains[ind], trains[i] = trains[i], trains[ind]
#         names[ind], names[i] = names[i], names[ind]
#         times[ind], times[i] = times[i], times[ind]

for i in range(1, N):
    train = trains[i]
    name = names[i]
    time = times[i]
    j = i - 1
    while j >= 0 and (name < names[j] or name == names[j] and time > times[j]):
        trains[j+1] = trains[j]
        names[j+1] = names[j]
        times[j+1] = times[j]
        j -= 1
    trains[j+1] = train
    names[j+1] = name
    times[j+1] = time
    
print(*trains, sep='\n')