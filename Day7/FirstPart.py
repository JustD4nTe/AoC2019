from itertools import permutations


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


def intcodeComputer(ampContrSoft, phaseSetting, inputSignal):
    programResult = 0
    # id in data[]
    dataOffset = 0

    # how many instructions program should skip
    # to get next opcode
    instructionOffset = 0

    while ampContrSoft[dataOffset] != 99:
        opcodeId, mode = parseOpcode(ampContrSoft[dataOffset])

        # calculation
        if opcodeId in [1, 2]:
            # position mode
            # (parameter is just a pointer to value)
            if mode[0] == 0:
                firstParameter = ampContrSoft[ampContrSoft[dataOffset + 1]]
            # immediate mode
            # (parameter is a value)
            else:
                firstParameter = ampContrSoft[dataOffset + 1]

            if mode[1] == 0:
                secondParameter = ampContrSoft[ampContrSoft[dataOffset + 2]]
            else:
                secondParameter = ampContrSoft[dataOffset + 2]

            thirdParameter = ampContrSoft[dataOffset + 3]

            # add
            if opcodeId == 1:
                result = firstParameter + secondParameter

            # multiply
            elif opcodeId == 2:
                result = firstParameter * secondParameter

            instructionOffset = 4
            ampContrSoft[thirdParameter] = result

        # input/output
        elif opcodeId in [3, 4]:
            # input
            if opcodeId == 3:
                # it's always in immediate mode
                # store at address *parameter*
                inputValue = phaseSetting if phaseSetting != 0 else inputSignal
                phaseSetting = 0
                ampContrSoft[ampContrSoft[dataOffset + 1]] = inputValue

            # output (error checks)
            elif opcodeId == 4:
                if mode[0] == 0:
                    parameter = ampContrSoft[ampContrSoft[dataOffset + 1]]
                else:
                    parameter = ampContrSoft[dataOffset + 1]
                print(parameter)
                programResult = parameter

            instructionOffset = 2

        # jumping
        elif opcodeId in [5, 6]:
            if mode[0] == 0:
                firstParameter = ampContrSoft[ampContrSoft[dataOffset + 1]]
            else:
                firstParameter = ampContrSoft[dataOffset + 1]

            if mode[1] == 0:
                secondParameter = ampContrSoft[ampContrSoft[dataOffset + 2]]
            else:
                secondParameter = ampContrSoft[dataOffset + 2]

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
                firstParameter = ampContrSoft[ampContrSoft[dataOffset + 1]]
            else:
                firstParameter = ampContrSoft[dataOffset + 1]

            if mode[1] == 0:
                secondParameter = ampContrSoft[ampContrSoft[dataOffset + 2]]
            else:
                secondParameter = ampContrSoft[dataOffset + 2]

            thirdParameter = ampContrSoft[dataOffset + 3]

            # less than
            if opcodeId == 7:
                if firstParameter < secondParameter:
                    ampContrSoft[thirdParameter] = 1
                else:
                    ampContrSoft[thirdParameter] = 0

            # equals
            elif opcodeId == 8:
                if firstParameter == secondParameter:
                    ampContrSoft[thirdParameter] = 1
                else:
                    ampContrSoft[thirdParameter] = 0

            instructionOffset = 4

        # oops..error :/
        else:
            str = "Something goes wrong!\n" + "opcode: " + str(
                opcodeId) + "\ncode \'line\': " + str(dataOffset)
            raise Exception(str)
            break

        dataOffset += instructionOffset

    return programResult


data = [int(i) for i in open("data.txt", 'r').readline().split(',')]

# get permutations of list
phaseSettings = permutations([4, 3, 2, 1, 0])

runNumber = 0
highestSignal = 0

# for every permutation
for phase in list(phaseSettings):
    print("Run: " + str(runNumber))
    output = 0

    # goes through all amplifiers
    for i in phase:
        try:
            output = intcodeComputer(data.copy(), i, output)
            
        # sometimes got exception, but all is under control ;)
        # just trust me :D
        except:
            break

    if output > highestSignal:
        highestSignal = output

    runNumber += 1

print("Highest signal: " + str(highestSignal))