

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

## Two's complement
def getTwosComp(argument):
    if (argument[0] == '1'):
        val = 65535 - int(argument, 2) + 1
        val = -val
    else:
        val = int(argument, 2)
    return int(val)

def getTwosComp32(argument):
    if (argument[0] == '1'):
        val = 2147483647 - int(argument, 2) + 1
        val = -val
    else:
        val = int(argument, 2)
    return int(val)


def Simulate():
    print("Welcome to the Simulation!")
    iFile = open("hex.txt", "r")
    oFile = open("output.txt.", "w")
    op =  ""
    rs = ""
    rt = ""
    rd = ""
    shamt = ""
    imm = ""
    funct = ""
    word = ""
    binary = ""
    newLine = ""
    Register = [ 0 for i in range(24)]
    Register[0] = 0
    for line in iFile:
        if (line == "\n" or line[0] == "#" ):
            continue
        if (str(line) == "0x1000ffff"):
            print("ThankYou")
            exit()
        word = word + line[2:10]        # get each line, but ignore 0x

        for i in word:
            binary = binary + hex2bin(i)    # convert to binary

        op = binary[0:6]

        if (op == "000000"):        # translate for add, addu, sub, slt, sll
            rs = binary[6:11]
            rt = binary[11:16]
            rd = binary[16:21]
            shamt = binary[21:26]
            funct = binary[26:32]
            opCode = getInstr(funct)
            # funct rd, rs, rt
            newLine = opCode + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + dec2regi(int(rt, 2))
            oFile.write(newLine)
            #updates the registers
            if (opCode == "addu"):
                Register[int(rd,2)] = Register[int(rs,2)] + Register[int(rt,2)]
            if (opCode == "sub"):
                Register[int(rd,2)] = Register[int(rs,2)] - Register[int(rt,2)]
            if (opCode == "slt"):
                if (Register[int(rs,2)] < Register[int(rt,2)]):
                    Register[int(rd,2)] = 1
                else:
                    Register[int(rd,2)] = 0
            if (opCode == "sll"): #this doesnot work right for some reason, need a fix
                (Register[int(rd,2)]) = Register[int(rt,2)] << int(shamt,2)
                if (Register[int(rd,2)] >  2147483647 ):
                    #a = Register[int(rd,2)]
                    #Register[int(rd,2)] = str(getTwosComp(Register[int(rd,2)]))
                    a =  bin(Register[int(rd,2)])[2:]
                    print(a)
                    #b = str(a)
                    print (getTwosComp32('10101011110111010000000000000000'))

        elif (op == "100011" or op == "101011"):      # translate lw or sw
            rs = binary[6:11]
            rt = binary[11:16]
            imm = binary[16:32]

            # op rt, imm(rs)
            #newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", 0x" + str(hex(int(imm, 2)))[2:].zfill(4)  + "(" + dec2regi(int(rs, 2)) + ")"
            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + "," + str(getTwosComp(imm))  + "(" + dec2regi(int(rs, 2)) + ")"
            oFile.write(newLine)
        elif (op == "000100" or op == "000101"):                   # translate for beq or bne
            rt = binary[6:11]
            rs = binary[11:16]
            imm = binary[16:32]

            # op rt, rs, imm
            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp(imm))
            oFile.write(newLine)

        else:                   # translate for addi, ori
            rs = binary[6:11]
            rt = binary[11:16]
            imm = binary[16:32]
            opCode = getInstr(op)
            # op rt, rs, imm
            newLine = opCode + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp(imm))
            oFile.write(newLine)
            #updates the registers
            if ( opCode == "addi"):
                Register[int(rt,2)] = Register[int(rs,2)] + int(imm,2)
            if(opCode == "ori"):
                Register[int(rt,2)] = Register[int(rs,2)] | int(imm,2)

        word = ""
        binary = ""
        oFile.write("\n")
    oFile.close()
    #prints the register contents
    print("Registers contents:", Register)
def main():

    userResponse = input("Would you like to begin Simulation? Enter yes or no: ")
    if (userResponse == "yes" or userResponse == "Yes"):
        Simulate()
    else:
        print("GoodBye")
if __name__== "__main__":
  main()
