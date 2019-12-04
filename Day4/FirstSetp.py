with open("data.txt", "r") as data:
    numberRange = data.readline().split("-")

numberInList = [int(i) for i in numberRange[0]]

number = int(numberRange[0])

count = 0

while number <= int(numberRange[1]):

    isNotDecrease = True
    haveDouble = False

    # Two adjacent digits are the same (like 22 in 122345).
    for i in range(len(numberInList) - 1):
        if numberInList[i] == numberInList[i+1]:
            haveDouble = True
            
        # Going from left to right, the digits never decrease; 
        # they only ever increase or stay the same (like 111123 or 135679).
        if numberInList[i] > numberInList[i+1]:
            isNotDecrease = False
            break
    
            
    if isNotDecrease and haveDouble:
        count += 1

    number += 1
    numberInList = [int(i) for i in str(number)]

print(count)