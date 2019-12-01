import math

def fuelCalculation(mass):
    temp = (math.floor(int(mass) / 3) - 2) 
    if temp > 0:
        return temp
    else:
        return 0

sum = 0

masses =  open("data.txt", "r").readlines()

for mass in masses:
    temp = fuelCalculation(mass)
    sum += temp
    while temp > 0:
        temp = fuelCalculation(temp)
        sum += temp


print(sum)

