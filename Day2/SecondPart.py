def InitializeMemory():
    return [int(i) for i in open("data.txt", 'r').readline().split(',')]

def RestoreGravityAssistProgram(firstInput, secondInput):
    memory = InitializeMemory()

    memory[1] = firstInput
    memory[2] = verb

    opcodeId = 0

    while memory[opcodeId] != 99:
        firstNumber = memory[memory[opcodeId + 1]]
        secondNumber = memory[memory[opcodeId + 2]]

        if memory[opcodeId] == 1:
            out = firstNumber + secondNumber
            
        elif memory[opcodeId] == 2:
            out = firstNumber * secondNumber

        # Can not handle a opcode different than 1,2 or 99
        else:
            break

        memory[memory[opcodeId + 3]] = out
        
        # Opcode, input, input, output
        opcodeId += 4

    # Output of program is stored in 0 address
    return memory[0]

programOutput = 0
noun = 0

while programOutput != 19690720:
    verb = 0
    
    while programOutput != 19690720:
        programOutput = RestoreGravityAssistProgram(noun, verb)
        if verb == 99:
            break
        verb += 1

    if noun == 99:
        break
    noun += 1
    
noun -= 1
verb -= 1

print("noun: " + str(noun) + "\tverb: " + str(verb)) 
print(100 * noun + verb)
