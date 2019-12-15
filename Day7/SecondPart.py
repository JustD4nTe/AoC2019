from itertools import permutations


class Amplifier:
    def __init__(self):
        pass

    def __init__(self, intcode, phaseSetting):
        self.intcode = intcode
        self.phaseSetting = phaseSetting
        self.mode = [0, 0, 0]
        self.opcode = 0

        # id in intcode[]
        self.dataOffset = 0

        # how many instructions program should skip
        # to get next opcode
        self.instructionOffset = 0

    # get opcode and parameters' modes
    # ABCDE
    # DE - two-digit opcode,
    #  C - mode of 1st parameter
    #  B - mode of 2nd parameter
    #  A - mode of 3rd parameter
    # omitted due to being a leading zero
    def parseOpcode(self, rawOpcode):
        rawOpcode = str(rawOpcode)
        # last two elements
        self.opcode = int(rawOpcode[-2:])

        # reverse list without two last elements
        # (we used them already)
        rawOpcode = rawOpcode[::-1][2:]

        self.mode = [
            int(rawOpcode[i:i + 1]) if rawOpcode[i:i + 1] != '' else 0
            for i in range(3)
        ]

    def computeIntcode(self, inputSignal):
        while self.intcode[self.dataOffset] != 99:
            self.parseOpcode(self.intcode[self.dataOffset])

            # calculation
            if self.opcode in [1, 2]:
                # position mode
                # (parameter is just a pointer to value)
                if self.mode[0] == 0:
                    firstParameter = self.intcode[self.intcode[self.dataOffset + 1]]
                # immediate mode
                # (parameter is a value)
                else:
                    firstParameter = self.intcode[self.dataOffset + 1]

                if self.mode[1] == 0:
                    secondParameter = self.intcode[self.intcode[self.dataOffset + 2]]
                else:
                    secondParameter = self.intcode[self.dataOffset + 2]

                thirdParameter = self.intcode[self.dataOffset + 3]

                # add
                if self.opcode == 1:
                    result = firstParameter + secondParameter

                # multiply
                elif self.opcode == 2:
                    result = firstParameter * secondParameter

                self.instructionOffset = 4
                self.intcode[thirdParameter] = result

            # input/output
            elif self.opcode in [3, 4]:
                # input
                if self.opcode == 3:
                    # it's always in immediate mode
                    # store at address *parameter*
                    inputValue = self.phaseSetting if self.phaseSetting != 0 else inputSignal
                    self.phaseSetting = 0
                    self.intcode[self.intcode[self.dataOffset + 1]] = inputValue

                    self.instructionOffset = 2

                # output (error checks)
                elif self.opcode == 4:
                    if self.mode[0] == 0:
                        outputValue = self.intcode[self.intcode[self.dataOffset +1]]
                    else:
                        outputValue = self.intcode[self.dataOffset + 1]


                    self.instructionOffset = 2
                    self.dataOffset += self.instructionOffset
                    
                    # "stops" computer and return computed value
                    return outputValue

            # jumping
            elif self.opcode in [5, 6]:
                if self.mode[0] == 0:
                    firstParameter = self.intcode[self.intcode[self.dataOffset + 1]]
                else:
                    firstParameter = self.intcode[self.dataOffset + 1]

                if self.mode[1] == 0:
                    secondParameter = self.intcode[self.intcode[self.dataOffset + 2]]
                else:
                    secondParameter = self.intcode[self.dataOffset + 2]

                # jump-if-true
                if self.opcode == 5:
                    if firstParameter != 0:
                        self.instructionOffset = 0
                        self.dataOffset = secondParameter
                    else:
                        self.instructionOffset = 3

                # jump-if-false
                elif self.opcode == 6:
                    if firstParameter == 0:
                        self.instructionOffset = 0
                        self.dataOffset = secondParameter
                    else:
                        self.instructionOffset = 3

            # comparison
            elif self.opcode in [7, 8]:
                if self.mode[0] == 0:
                    firstParameter = self.intcode[self.intcode[self.dataOffset + 1]]
                else:
                    firstParameter = self.intcode[self.dataOffset + 1]

                if self.mode[1] == 0:
                    secondParameter = self.intcode[self.intcode[self.dataOffset + 2]]
                else:
                    secondParameter = self.intcode[self.dataOffset + 2]

                thirdParameter = self.intcode[self.dataOffset + 3]

                # less than
                if self.opcode == 7:
                    if firstParameter < secondParameter:
                        self.intcode[thirdParameter] = 1
                    else:
                        self.intcode[thirdParameter] = 0

                # equals
                elif self.opcode == 8:
                    if firstParameter == secondParameter:
                        self.intcode[thirdParameter] = 1
                    else:
                        self.intcode[thirdParameter] = 0

                self.instructionOffset = 4

            # oops..error :/
            else:
                str = "Something goes wrong!\n" + "opcode: " + str(
                    self.opcode) + "\ncode \'line\': " + str(self.dataOffset)
                raise Exception(str)

            self.dataOffset += self.instructionOffset

        return None


intcode = [int(i) for i in open("data.txt", 'r').readline().split(',')]

# get permutations of list
phaseSettings = permutations([9, 8, 7, 6, 5])

runNumber = 0
highestSignal = 0

amplifiers = [0] * 5

# for every permutation
for phase in list(phaseSettings):
    print("Run: " + str(runNumber))

    output = 0

    # initialize every amplifier
    for i in range(5):
        amplifiers[i] = Amplifier(intcode.copy(), phase[i])

    runNumber += 1

    # output form last amplifier goes to first amplifier
    # but when outpu is None previous output is "correct"
    while True:
        # goes through all amplifiers
        try:
            for amplifier in amplifiers:
                temp = amplifier.computeIntcode(output)

                output = temp if temp != None else output

                if temp == None:
                    break

            if temp == None:
                break

        # sometimes got exception, but all is under control ;)
        # just trust me :D
        except:
            continue

    if output > highestSignal:
        highestSignal = output

print("Highest signal: " + str(highestSignal))