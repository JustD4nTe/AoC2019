# get opcode and parameters' modes
# ABCDE
# DE - two-digit opcode,
#  C - mode of 1st parameter
#  B - mode of 2nd parameter
#  A - mode of 3rd parameter
# omitted due to being a leading zero
def parseOpcode(rawOpcode):
    rawOpcode = str(rawOpcode)
    # last two elements
    opcode = int(rawOpcode[-2:])

    # reverse list without two last elements 
    # (we used them already)
    rawOpcode = rawOpcode[::-1][2:]

    mode = [int(rawOpcode[i:i+1]) if rawOpcode[i:i+1]
            != '' else 0 for i in range(3)]

    return opcode, mode


data = [int(i)
        for i in open("data.txt", 'r').readline().split(',')]

# id in ^data[]
dataOffset = 0

# how many instructions program should skip
# to get next opcode
instructionOffset = 0

while data[dataOffset] != 99:
    opcodeId, mode = parseOpcode(data[dataOffset])

    # calculation
    if opcodeId in [1, 2]:
        # position mode 
        # (parameter is just a pointer to value)
        if mode[0] == 0:
            firstParameter = data[data[dataOffset + 1]]
        # immediate mode
        # (parameter is a value)
        else:
            firstParameter = data[dataOffset + 1]

        if mode[1] == 0:
            secondParameter = data[data[dataOffset + 2]]
        else:
            secondParameter = data[dataOffset + 2]

        thirdParameter = data[dataOffset + 3]

        # add
        if opcodeId == 1:
            result = firstParameter + secondParameter

        # multiply
        elif opcodeId == 2:
            result = firstParameter * secondParameter

        instructionOffset = 4
        data[thirdParameter] = result

    # input/output
    elif opcodeId in [3, 4]:
        # input
        if opcodeId == 3:
            # it's always in immediate mode
            # store at address *parameter*
            data[data[dataOffset + 1]] = int(input("input: "))

        # output (error checks)
        elif opcodeId == 4:
            if mode[0] == 0:
                parameter = data[data[dataOffset + 1]]
            else:
                parameter = data[dataOffset + 1]
            print(parameter)

        instructionOffset = 2

    # jumping
    elif opcodeId in [5, 6]:
        if mode[0] == 0:
            firstParameter = data[data[dataOffset + 1]]
        else:
            firstParameter = data[dataOffset + 1]

        if mode[1] == 0:
            secondParameter = data[data[dataOffset + 2]]
        else:
            secondParameter = data[dataOffset + 2]

        # jump-if-true
        if opcodeId == 5:
            if firstParameter != 0:
                instructionOffset = 0
                dataOffset = secondParameter
            else:
                instructionOffset = 3

        # jump-if-false
        elif opcodeId == 6:
            if firstParameter == 0:
                instructionOffset = 0
                dataOffset = secondParameter
            else:
                instructionOffset = 3

    # comparison
    elif opcodeId in [7, 8]:
        if mode[0] == 0:
            firstParameter = data[data[dataOffset + 1]]
        else:
            firstParameter = data[dataOffset + 1]

        if mode[1] == 0:
            secondParameter = data[data[dataOffset + 2]]
        else:
            secondParameter = data[dataOffset + 2]

        thirdParameter = data[dataOffset + 3]

        # less than
        if opcodeId == 7:
            if firstParameter < secondParameter:
                data[thirdParameter] = 1
            else:
                data[thirdParameter] = 0

        # equals
        elif opcodeId == 8:
            if firstParameter == secondParameter:
                data[thirdParameter] = 1
            else:
                data[thirdParameter] = 0

        instructionOffset = 4

    # oops..error :/
    else:
        print("Something goes wrong!")
        print("opcode: " + str(opcodeId))
        print("code \'line\': " + str(dataOffset))
        break

    dataOffset += instructionOffset
