# Function for converting hex to binary
def hex2bin(argument):
    switcher = {
        '0': "0000",
        '1': "0001",
        '2': "0010",
        '3': "0011",
        '4': "0100",
        '5': "0101",
        '6': "0110",
        '7': "0111",
        '8': "1000",
        '9': "1001",
        'a': "1010",
        'b': "1011",
        'c': "1100",
        'd': "1101",
        'e': "1110",
        'f': "1111",
    }
    return switcher.get(argument, "nothing")

## Table for all instruction opcodes
def getInstr(argument):
    switcher = {
        "001000": "addi",
        "100001": "addu",
        "101011": "sw",
        "100000": "add",
        "101010": "slt",
        "100100": "and",
        "100101": "or",
        "000000": "sll",
        "000010": "srl",
        "100110": "xor",
        "000100": "beq",
        "000101": "bne",
        "100011": "lw",
        "100010": "sub",
        "001101": "ori",
        "001111": "lui",
    }
    return switcher.get(argument, "nothing")

## Table for all instruction registers
def dec2regi(argument):
    switcher = {
        '0': "$0",
        '1': "$1",
        '2': "$2",
        '3': "$3",
        '4': "$4",
        '5': "$5",
        '6': "$6",
        '7': "$7",
        '8': "$8",
        '9': "$9",
        '10': "$10",
        '11': "$11",
        '12': "$12",
        '13': "$13",
        '14': "$14",
        '15': "$15",
        '16': "$16",
        '17': "$17",
        '18': "$18",
        '19': "$19",
        '20': "$20",
        '21': "$21",
        '22': "$22",
        '23': "$23",
    }
    return switcher.get(str(argument), "nothing")

## Two's complement for 16 bits
def getTwosComp16(argument):
    if (argument[0] == '1'):
        num = int(argument,2)
        val = -32768 +(num - 32768)
    else:
        val = int(argument, 2)
    return int(val)

## Two's complement for 32 bits
def getTwosComp32(argument):
    if (argument[0] == '1'):
        num = int(argument,2)
        val = -2147483648 + (num - 2147483648)
    else:
        val = int(argument, 2)
    return int(val)

## Returns bit size of a non-negative number
def getBitSize(argument):
    sum = 0
    while argument >> sum:
        sum += 1

    return sum

## Inserts new instruction so long as there is no duplicates on the same PC
def insertList(pc, newline):
    check = False

    for a, b in printList:
        if (a == pc and b == newline):
            check = True

    if (check == False):
        printList.append((pc, newline))

## Returns the proper memory index of the memory address
def memoryIndex(val,offset1):
    val = val + (offset1)
    index = (val - 8192)/4
    return int (index)

Register = [0 for i in range(24)]
printList = []

def Simulate(I):
    oFile = open("output.txt.", "w")
    print("Welcome to the Simulation!")
    op =  ""
    rs = ""
    rt = ""
    rd = ""
    shamt = ""
    imm = ""
    funct = ""
    newLine = ""

    Memory = [0 for i in range(508)]            # list for memory content
    PC = 0
    instructionCount = 0

    finished = False
    while(not(finished)):
        Register[0] = 0
        binary = I[PC]
        if (binary == "00010000000000001111111111111111"):   # END instruction
            finished = True

        op = binary[0:6]
        rSyntax = True         # checker if syntax is ArithLog (True) or Shift (False)

        # translate for add, addu, sub, slt, sll
        if (op == "000000"):
            rs = binary[6:11]
            rt = binary[11:16]
            rd = binary[16:21]
            shamt = binary[21:26]
            funct = binary[26:32]
            opCode = getInstr(funct)

            #updates the registers
            if (opCode == "addu"):
                Register[int(rd,2)] = Register[int(rs,2)] + Register[int(rt,2)]

            elif (opCode == "add"):
                Register[int(rd,2)] = Register[int(rs,2)] + Register[int(rt,2)]

            elif (opCode == "sub"):
                Register[int(rd,2)] = Register[int(rs,2)] - Register[int(rt,2)]

            elif (opCode == "and"):
                Register[int(rd,2)] = Register[int(rs,2)] & Register[int(rt,2)]

            elif (opCode == "xor"):
                Register[int(rd,2)] = Register[int(rs,2)] ^ Register[int(rt,2)]

            elif (opCode == "slt"):
                temp1 = Register[int(rs,2)]
                temp2 = Register[int(rt,2)]

                if (temp1 > 2147483648):
                    lol = bin(temp1)[2:]
                    temp1 = getTwosComp32(lol)

                if (temp2 > 2147483648):
                    lol1 = bin(temp2)[2:]
                    temp2 = getTwosComp32(lol1)

                if (temp1 < temp2):
                    Register[int(rd,2)] = 1
                else:
                    Register[int(rd,2)] = 0

            elif (opCode == "sll"):
                imm1 = Register[int(rt,2)] << int(shamt,2)

                if (imm1 < -2147483648):
                    hold = bin(imm1)[3:]

                    imm1 = getTwosComp32(hold)
                    Register[int(rd,2)] = -(imm1)

                elif (imm1 >= 2147483648):
                    temp = bin(imm1)[2:]
                    imm1 = getTwosComp32(temp)
                    Register[int(rd,2)] = imm1

                else:
                    Register[int(rd,2)] = imm1
                    
                rSyntax = False

            elif (opCode == "srl"):
                Register[int(rd,2)] = Register[int(rt,2)] >> int(shamt,2)
                temp = bin(Register[int(rd,2)])

                if (temp[0] == '-'):
                    Register[int(rd,2)] = abs(Register[int(rd,2)])

                    ogBitSize = getBitSize(Register[int(rd,2)])
                    val = Register[int(rd,2)] ^ 268435455                   # get the
                    val += 1                                                # two's complement

                    if(ogBitSize > getBitSize(val)):                        # check if there are missing zeroes
                        zeroes = ogBitSize - getBitSize(val)
                        temp = bin(val)[2:]
                        while zeroes!=0:                                    # concatanate the missing zeroes
                            temp = '0' + temp
                            zeroes -= 1
                        temp = '1' + temp

                    Register[int(rd,2)] = int(temp, 2)

                rSyntax = False

            if (rSyntax):
                # funct rd, rs, rt              ArithLog
                newLine = opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + dec2regi(int(rt, 2))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + dec2regi(int(rt, 2))
                print(pr)
                instructionCount+=1
            else:
                # funct rd, rt, shamt           Shift
                newLine = opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rt, 2)) + ", " + str(int(shamt, 2))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rt, 2)) + ", " + str(int(shamt, 2))
                print(pr)
                instructionCount+=1

            insertList(PC, newLine)
            PC += 4

        elif (op == "100011" or op == "101011"):      # translate lw or sw
            rs = binary[6:11]
            rt = binary[11:16]
            imm = binary[16:32]

            # op rt, imm(rs)
            if (op == "101011"):
                newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + "," + str(getTwosComp16(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
                pr = "PC"+ ": " + str(PC) + " "+  getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + str(getTwosComp16(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
                print(pr)
                instructionCount+=1
                num = Register[int(rs,2)]
                im = getTwosComp16(imm)
                Memory[memoryIndex(num,im)] = Register[int(rt,2)]

            else:
                newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + "," + str(getTwosComp16(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
                pr = "PC"+ ": " + str(PC) + " "+  getInstr(op) + " " + dec2regi(int(rt, 2)) + "," + str(getTwosComp16(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
                print(pr)
                instructionCount+=1
                num = Register[int(rs,2)]
                im = getTwosComp16(imm)
                Register[int(rt,2)] = Memory[memoryIndex(num,im)]

            insertList(PC, newLine)
            PC += 4

        elif (op == "000100" or op == "000101"):                   # translate for beq or bne
            rt = binary[6:11]
            rs = binary[11:16]
            imm = binary[16:32]

            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp16(imm))
            pr = "PC"+ ": " + str(PC) + " "+  getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp16(imm))
            print(pr)
            instructionCount+=1

            insertList(PC, newLine)

            # op rt, rs, imm
            if (op == "000100"):
                offset = getTwosComp16(imm)
                if (Register[int(rs,2)] == Register[int(rt,2)]):
                    PC = PC + 4 + (4*offset)

                else:
                    PC = PC + 4
                    
            elif(op == "000101"):
                offset = getTwosComp16(imm)
                if (Register[int(rs,2)] != Register[int(rt,2)]):
                    PC = PC + 4 + (4*offset)
                    
                elif(Register[int(rs,2)] == Register[int(rt,2)]):
                    PC = PC + 4
                    
        else:                                                       # translate for addi, ori, lui
            rs = binary[6:11]
            rt = binary[11:16]
            imm = binary[16:32]
            opCode = getInstr(op)

            # updates the registers             op rt, rs, imm
            if ( opCode == "addi"):
                Register[int(rt,2)] = Register[int(rs,2)] + getTwosComp16(imm)
                newLine = opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp16(imm))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp16(imm))
                print(pr)
                instructionCount+=1

            elif (opCode == "ori"):
                Register[int(rt,2)] = Register[int(rs,2)] | int(imm,2)
                newLine = opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(int(imm,2))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(int(imm,2))
                print(pr)
                instructionCount+=1
                
            elif (opCode == "lui"):
                imm = getTwosComp16(imm)
                Register[int(rt, 2)] = imm << 16
                newLine = opCode + " " + dec2regi(int(rt,2)) + ", " + str(imm)
                pr = "PC: " + str (PC) + " " + opCode + " " + dec2regi(int(rt,2)) + ", " + str(imm)
                print(pr)
                instructionCount+=1

            insertList(PC, newLine)
            PC += 4

    print("\nRegister Contents: ", Register)
    print("Memory Array: ", Memory)
    print("Total Instructions Count: ",instructionCount)

    # Write all instructions to an output file
    printList.sort()
    for a, b in printList:
        oFile.write(b + "\n")

    oFile.close()


def main():
    iFile = open("group_3_p2_prpg.txt", "r")
    I  = []
    binary = ""
    word = ""

    for line in iFile:
        if (line == "\n" or line[0] == "#" ):
            continue
        if (line == "0x1000ffff"):
            # prints the register contents
            print("Registers contents:", Register)
            print("\nThankYou")
            exit()

        word = word + line[2:10]        # get each line, but ignore 0x

        for i in word:
            binary = binary + hex2bin(i)    # convert to binary
        I.append(binary)
        I.append(0)
        I.append(0)
        I.append(0)
        word = ""
        binary =""
    Simulate(I)
    print("\n***SIMULATION FINISHED***")

if __name__== "__main__":
  main()
