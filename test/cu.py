# # y = 5x^2 - 20x + 2

# x = int(input("Enter the value of x: "))
# # y = 5 * x**2 - 20 * x + 2
# y = 5*(x**2) - (20*x) + 2
# print(f"The value of y is: {y}")


# while True:
#     point = float(input("Enter the point: "))
#     if point >= 90:
#         print("A")
#     elif point >= 70 and point < 90:
#         print("B")
#     elif point >= 50 and point < 70:
#         print("C")
#     else :
#         print("Fail")

# n = int(input("n : "))
# x = int(input("x : "))
# m = int(input("m : "))

# save = []
# answer = 0

# for i in range(n):
#     save.append(x)
#     x = x * m
    
# for i in range(len(save)):
#     print(save[i])
#     answer = answer + save[i]
    
# print(answer)

# def isSevenUp(x):
#     if x % 7 == 0 or 7" in str(x):
#         return True
#     else:
#         return False

# def nextSevenUp(x):
#     if not x % 7 == 0:
#         while True:
#             x = x + 1
#             # print(x)
#             if x % 7 == 0 or "7" in str(x):
#                 break
#         # print(f"answer : {x}")
#         return x

# exec(input().strip())

# print(isSevenUp(14))
# print(isSevenUp(95))
# print(nextSevenUp(60))
# print(nextSevenUp(-10))

# a,b,c,d = [int(e) for e in input().split()]

# # print(a,b,c,d)
# # print(b)
# # print(c)
# # print(d)

# if a > b :
#     b = a
#     while d >= a :
#         if c > d :
#             a = a + 1
#         else :
#             d = d - 1
# else :
#     if c % 2 == 0:
#         d = d + a
#     else:
#         if d > c :
#             c = c + d
#         else :
#             b = b + a
#     a = b + c

# print(a,b,c,d)

save = []
sum = 0
answer2 = 0

turn = int(input("count of turn : "))
for i in range(turn):
    data = float(input())
    # print(data)
    save.append(data)
print(f"test bug : save = {save}")

for i in range(len(save)):
    sum = sum + save[i]

answer1 = sum / len(save)
    
print(f"test bug : answer1 = {answer1}")

# print(f"test bug : save = {len(save)}")

for i in range(len(save)):
    answer2 = (answer2 + ((sum + save[i]) - answer1 ))**2 

print(f"test bug : answer2 = {answer2}")
import math

sd = math.sqrt(answer2 / len(save))

print(f"test bug : sd = {sd}")


# print(f"average = {answer1}, sd = {round(answer2,5)} ")


# round(answer ,5)

# import math

# save = []
# sum_data = 0
# answer2 = 0

# turn = int(input("Enter the count of turns: "))
# for i in range(turn):
#     data = float(input(f"Enter data {i+1}: "))
#     save.append(data)

# # คำนวณค่าเฉลี่ย
# sum_data = sum(save)
# average = sum_data / len(save)

# # คำนวณค่า SD
# for i in range(len(save)):
#     answer2 += (save[i] - average) ** 2

# # หาค่าเบี่ยงเบนมาตรฐาน (SD)
# sd = math.sqrt(answer2 / len(save))

# # แสดงผลลัพธ์
# print(f"average = {round(average, 5)}, sd = {round(sd, 5)}")
