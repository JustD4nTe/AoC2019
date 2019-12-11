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

    mode = [
        int(rawOpcode[i:i + 1]) if rawOpcode[i:i + 1] != '' else 0
        for i in range(3)
    ]

    return opcode, mode

# get parameter from intcode by proper mode
def getParameter(mode, offset):
    # position mode
    # (parameter is just a pointer to value)
    if mode == 0:
        return data[data[offset]]

    # immediate mode
    # (parameter is a value)
    elif mode == 1:
        return data[offset]

    # relative mode
    # (similar to position mode,
    #  but additionally take relativeBase into account)
    elif mode == 2:
        return data[data[offset] + relativeBase]

    return None

# get address which will be used to write a "thing"
def getAddressToWrite(mode, offset):
    if mode == 0:
        return data[offset]

    # writing is not working in immediate mode
    elif mode == 1:
        print("invalid")
        return None

    elif mode == 2:
        return data[offset] + relativeBase
    
    return None


data = [int(i) for i in open("data.txt", 'r').readline().split(',')] + [0] * 1000

# id in ^data[]
dataOffset = 0

# how many instructions program should skip
# to get next opcode
instructionOffset = 0

relativeBase = 0

while data[dataOffset] != 99:
    opcodeId, mode = parseOpcode(data[dataOffset])

    # calculation
    if opcodeId in [1, 2]:
        firstParameter = getParameter(mode[0], dataOffset + 1)
        secondParameter = getParameter(mode[1], dataOffset + 2)         
        thirdParameter = getAddressToWrite(mode[2], dataOffset + 3)

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
            parameter = getAddressToWrite(mode[2], dataOffset + 3)
            data[parameter] = int(input("input: "))


        # output (error checks)
        elif opcodeId == 4:
            print(getParameter(mode[0], dataOffset + 1))

        instructionOffset = 2

    # jumping
    elif opcodeId in [5, 6]:
        firstParameter = getParameter(mode[0], dataOffset + 1)
        secondParameter = getParameter(mode[1], dataOffset + 2) 

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
        firstParameter = getParameter(mode[0], dataOffset + 1)
        secondParameter = getParameter(mode[1], dataOffset + 2) 
        thirdParameter = getAddressToWrite(mode[2], dataOffset + 3)

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
    
    # adjusts the relative base
    elif opcodeId == 9:
        relativeBase += getParameter(mode[0], dataOffset +1)
        instructionOffset = 2

    # oops..error :/
    else:
        print("Something goes wrong!")
        print("opcode: " + str(opcodeId))
        print("code \'line\': " + str(dataOffset))
        break

    dataOffset += instructionOffset