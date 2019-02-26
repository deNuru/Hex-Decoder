# function for converting hex to binary
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
        val = 65535 - int(argument, 2) + 1
        val = -val
    else:
        val = int(argument, 2)
    return int(val)

## Two's complement for 32 bits
def getTwosComp32(argument):
    if (argument[0] == '1'):
        val = 4294967295 - int(argument, 2) + 1
        val = -val
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

Register = [ 0 for i in range(24)]
printList = []

def Simulate(I):
    oFile = open("output.txt.", "w")
    print("Welcome to the Simulation!")
    iFile = open("hex.txt", "r")
    op =  ""
    rs = ""
    rt = ""
    rd = ""
    shamt = ""
    imm = ""
    funct = ""
    newLine = ""

    PC = 0

    finished = False
    while(not(finished)):
        Register[0] = 0
        binary = I[PC]
        if (binary == "00010000000000001111111111111111"):   # END instruction
            finished = True
            print("***Simulation finished***")

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

            elif (opCode == "sub"):
                Register[int(rd,2)] = Register[int(rs,2)] - Register[int(rt,2)]

            elif (opCode == "and"):
                Register[int(rd,2)] = Register[int(rs,2)] & Register[int(rt,2)]
                print("Register 12 = ", (Register[12]))

            elif (opCode == "slt"):
                if (Register[int(rs,2)] < Register[int(rt,2)]):
                    Register[int(rd,2)] = 1
                else:
                    Register[int(rd,2)] = 0

            elif (opCode == "sll"):
                Register[int(rd,2)] = Register[int(rt,2)] << int(shamt,2)
                rSyntax = False

            elif (opCode == "srl"):
                Register[int(rd,2)] = Register[int(rt,2)] >> int(shamt,2)
                temp = bin(Register[int(rd,2)])
                if (temp[0] == '-'):
                    Register[int(rd,2)] = abs(Register[int(rd,2)])

                    ogBitSize = getBitSize(Register[int(rd,2)])
                    val = Register[int(rd,2)] ^ 268435455
                    val += 1

                    if(ogBitSize > getBitSize(val)):
                        zeroes = ogBitSize - getBitSize(val)
                        temp = bin(val)[2:]
                        while zeroes!=0:
                            temp = '0' + temp
                            zeroes -= 1
                        temp = '1' + temp

                    Register[int(rd,2)] = int(temp, 2)
                    print("Current", (Register[int(rd,2)]))

                rSyntax = False

            if (rSyntax):
                # funct rd, rs, rt              ArithLog
                newLine = opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + dec2regi(int(rt, 2))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + dec2regi(int(rt, 2))
                print(pr)
                PC = PC + 4
                print("Registers contents:", Register)
            else:
                # funct rd, rt, shamt           Shift
                newLine = opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rt, 2)) + ", " + str(int(shamt, 2))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rt, 2)) + ", " + str(int(shamt, 2))
                print(pr)
                PC = PC + 4
                print("Registers contents:", Register)

            insertList(PC, newLine)

        elif (op == "100011" or op == "101011"):      # translate lw or sw
            rs = binary[6:11]
            rt = binary[11:16]
            imm = binary[16:32]

            # op rt, imm(rs)
            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + "," + str(getTwosComp16(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
            pr = "PC"+ ": " + str(PC) + " "+  getInstr(op) + " " + dec2regi(int(rt, 2)) + "," + str(getTwosComp16(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
            print(pr)
            PC = PC + 4
            print("Registers contents:", Register)
            insertList(PC, newLine)
            
        elif (op == "000100" or op == "000101"):                   # translate for beq or bne
            rt = binary[6:11]
            rs = binary[11:16]
            imm = binary[16:32]
            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp16(imm))
            pr = "PC"+ ": " + str(PC) + " "+  getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp16(imm))
            print(pr)
            # op rt, rs, imm
            if (op == "000100"):
                offset = getTwosComp16(imm)
                if (Register[int(rs,2)] == Register[int(rt,2)]):
                    PC = PC + 4 + (4*offset)
                    print("Registers contents:", Register)
                else:
                    PC = PC + 4
                    print("Registers contents:", Register)
            elif(op == "000101"):
                offset = getTwosComp16(imm)
                if (Register[int(rs,2)] != Register[int(rt,2)]):
                    PC = PC + 4 + (4*offset)
                    print("Registers contents:", Register)
                elif(Register[int(rs,2)] == Register[int(rt,2)]):
                    PC = PC + 4
                    print("Registers contents:", Register)
            
            insertList(PC, newLine)

        else:                   # translate for addi, ori
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
                PC = PC + 4
                print("Registers contents:", Register)
            if(opCode == "ori"):
                Register[int(rt,2)] = Register[int(rs,2)] | int(imm,2)
                newLine = opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(int(imm,2))
                pr = "PC"+ ": " + str(PC) + " "+  opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(int(imm,2))
                print(pr)
                PC = PC + 4
                print("Registers contents:", Register)
            
            insertList(PC, newLine)
    
    # Write all instructions to an output file
    for a, b in printList:
        oFile.write(b)
        oFile.write("\n")

    oFile.close()


def main():
    iFile = open("hex.txt", "r")
    oFile = open("output.txt.", "w")
    I  = []
    binary = ""
    word = ""
    #userResponse = input("Would you like to begin Simulation? Enter yes or no: ")
    #if (userResponse == "yes" or userResponse == "Yes"):
    for line in iFile:
        if (line == "\n" or line[0] == "#" ):
            continue
        if (str(line) == "0x1000ffff"):
            #prints the register contents
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
    #else:
        #print("GoodBye")
if __name__== "__main__":
  main()
