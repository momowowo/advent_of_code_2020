import argparse
import sys

#Set up arguments and read them in
parser = argparse.ArgumentParser()
parser.add_argument('file', help="File containing input code. Required.")
args, unknown = parser.parse_known_args()

#Set up variables
file = args.file
instructions_list = []

def str2int(i):
    if i[0] == '+':
        return int(i[1:])
    else:
        return int(i)

def str2int_inverse(i):
    if i[0] == '+':
        return int("-" + i[1:])
    else:
        return int(i[1:])

def testCode(instructions_list, runFrom, accumulate):
    x = runFrom
    numlines = len(instructions_list)

    while x < numlines:
        (command, argument, counter) = instructions_list[x]
        # Check counter to make sure it's the first time we are executing this line of instruction
        if counter == 1:
            break
        elif counter > 1:
            sys.exit("ERROR: Unexpected counter value while testing code")

        #Update the instruction counter, as we will be incrementing x in the next step
        instructions_list[x][2] += 1

        #Execute the line of code
        if command == 'acc':
            accumulate += str2int(argument)
            x += 1
        elif command == 'jmp':
            x += str2int(argument)
        elif command == 'nop':
            x += 1
        else:
            sys.exit("ERROR: invalid command") 

    if x == numlines:
        #If you reach this line, the code finished executing
        print("Normal program termination. The value of the accumulator was: " + str(accumulate))
        return True
    else:
        return False



try:
    with open(file) as f:
        #Read the file all into one list
        print("Reading in file...")
        lines = f.readlines()
        numlines = len(lines)
        
        #For each line, parse the instruction into the command and argument, add a counter, and write into a new list
        for line in lines:
            #print("Parsing line: " + line.strip())
            command, argument = line.split(" ")
            instruction = [command, argument, 0]
            instructions_list.append(instruction)

        #Now attempt to execute each instruction in the proper order
        accumulator = 0
        x = 0
        runOrder = []

        while x < numlines:
            fixed = False
            (command, argument, counter) = instructions_list[x]
            # Check counter to make sure it's the first time we are executing this line of instruction
            if counter == 1:
                print("Infinite loop detected. The value of the accumulator was " + str(accumulator))

                runOrder.pop() #Remove this current instruction since we are not executing it
                
                #Backtracking to fix
                while (len(runOrder) > 0):            
                    
                    #Go back to the last operation before it and perform the "fixed" version
                    lastX = runOrder[-1]
                    (command, argument, counter) = instructions_list[lastX]
                    if command == 'jmp':
                        #Do nop instead
                        x = lastX + 1
                    elif command == 'nop':
                        #Do jmp instead
                        x = lastX + str2int(argument)
                    elif command == 'acc':
                        #Adjust accumulator since we are going to re-execute this instruction below
                        accumulator += str2int_inverse(argument)
                        x = lastX + 1

                    # Test if the program will finish executing normally with this change
                    if testCode(instructions_list, x, accumulator):
                        print("Fixed line " + str(lastX + 1) + ": " + command + " " + argument.strip() + " => " + ("nop " if (command == "jmp") else "jmp ") + argument.strip())
                        fixed = True
                        break
                    else:
                        #Backtrack to the previous command and test from there
                        runOrder.pop()
            
            if fixed == True:
                break

            elif counter > 1:
                sys.exit("ERROR: Unexpected counter value while executing commands")

            #Update the instruction counter and run order first, as we will be incrementing x in the next step
            instructions_list[x][2] += 1
            runOrder.append(x)

            #Execute the line of code
            if command == 'acc':
                accumulator = accumulator + str2int(argument)
                x += 1
            elif command == 'jmp':
                x += str2int(argument)
            elif command == 'nop':
                x += 1
            else:
                sys.exit("ERROR: invalid command") 

        if x == numlines:
            #If you reach this line, the code finished executing
            print("Normal program termination. The value of the accumulator was " + str(accumulator))
            

except (OSError, IOError) as e:
  print("ERROR: Could not open file")

