#!/usr/bin/python3.10.2 專案一開始

import random
#猜數字遊戲
min = 1
max = 10
count = 0
target = random.randint(min,max)
print("=============猜數字遊戲==================\n\n")

while True:
    keyin = int(input(f'猜數字範圍{min}~{max}:'))
    count += 1
    if (keyin == target):
        print(f'賓果!猜對了，答案是:{target}')
        print(f'你共猜了{count}次')
        break
    else:
        print("猜錯了!")
        print(f'您已經猜了{count}次')
print('遊戲結束')
