data = [int(i) for i in open("data.txt", 'r').readline().split(',')]
data[1] = 12
data[2] = 2

opcodeId = 0

while data[opcodeId] != 99:
    firstNumber = data[data[opcodeId + 1]]
    secondNumber = data[data[opcodeId + 2]]

    if data[opcodeId] == 1:
        out = firstNumber + secondNumber
        
    elif data[opcodeId] == 2:
        out = firstNumber * secondNumber

    else:
        print("Something goes wrong!")
        print("OpcodeId: " + str(opcodeId))
        print("Program dump: " + str(data))
        break

    data[data[opcodeId + 3]] = out
    opcodeId += 4

print(str(data))