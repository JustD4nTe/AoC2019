import math

sum = 0

masses =  open("data.txt", 'r').readlines()

for mass in masses:
    sum += (math.floor(int(mass) / 3) - 2)

print(sum)