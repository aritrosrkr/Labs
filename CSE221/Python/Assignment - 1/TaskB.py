T = int(input())
for i in range(T):
    x = input()
    x = x.split(' ')
    if '+' in x:
        print(float(x[1]) + float(x[3]))
    elif '-' in x:
        print(float(x[1]) - float(x[3]))
    elif '*' in x:
        print(float(x[1]) * float(x[3]))
    elif '/' in x:
        print(float(x[1]) / float(x[3]))