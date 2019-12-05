with open("data.txt", "r") as data:
    numberRange = data.readline().split("-")

numberInList = [int(i) for i in numberRange[0]]

number = int(numberRange[0])

count = 0

while number <= int(numberRange[1]):

    isNotDecrease = True
    haveDouble = False

     # Two adjacent digits are the same (like 22 in 122345).

    # compare 3 last digits
    if numberInList[-3] != numberInList[-2] == numberInList[-1]:
        haveDouble = True

    # compare 3 first digits
    elif numberInList[0] == numberInList[1] != numberInList[2]:
        haveDouble = True

    else:       
        for i in range(1, len(numberInList) - 2):
            if numberInList[i-1] != numberInList[i] == numberInList[i+1] != numberInList[i+2]:
                haveDouble = True
                break
    # Going from left to right, the digits never decrease; 
    # they only ever increase or stay the same (like 111123 or 135679).    
    for i in range(len(numberInList) - 1):
        if numberInList[i] > numberInList[i+1]:
            isNotDecrease = False
            break


    if isNotDecrease and haveDouble:
        count += 1

    number += 1
    numberInList = [int(i) for i in str(number)]

print(count)