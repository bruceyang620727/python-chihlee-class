#!/usr/bin/python3.10.2 專案一開始

import random
#猜數字遊戲
min = 1
max = 100
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
    elif keyin > target:
        print("再小一點")
        max = keyin - 1
    elif keyin < target:
        print("再大一點")
        min = keyin + 1
        print(f"你已經猜了{count}次了!")    

print("遊戲結束了!下次見")


