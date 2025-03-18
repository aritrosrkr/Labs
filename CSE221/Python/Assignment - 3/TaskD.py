T = int(input())

# def recursive_sum(a, n, m):
#     if n == 1:
#         return a % m
    
#     if n % 2 == 0:
#         half_sum = recursive_sum(a, n//2, m)
#         ans = 1
#         x = a
#         i = n//2
#         while i > 0:
#             if i % 2 != 0:
#                 ans = (x * ans) % m
#             i = i // 2
#             x = (x * x) % m
#         return (half_sum * (1 + ans)) % m
    
#     else:
#         prev_sum = recursive_sum(a, n-1, m)
#         ans = 1
#         x = a
#         i = n
#         while i > 0:
#             if i % 2 != 0:
#                 ans = (x * ans) % m
#             i = i // 2
#             x = (x * x) % m
#         return (prev_sum + ans) % m
    
# for t in range(T):
#     a, n, m = map(int, input().split())
#     print(recursive_sum(a, n, m))

for t in range(T):
    a, n, m = map(int, input().split())
    sum = 0
    x = 1
    for i in range(1, n+1):
        x = (x * a) % m
        sum = (sum + x) % m 
    print(sum)
    