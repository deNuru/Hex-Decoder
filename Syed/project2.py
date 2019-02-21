

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

        if (op == "000000"):        # translate for add
            rs = binary[6:11]
            rt = binary[11:16]
            rd = binary[16:21]
            shamt = binary[21:26]
            funct = binary[26:32]

            # funct rd, rs, rt
            newLine = getInstr(funct) + " " + dec2regi(int(rd, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + dec2regi(int(rt, 2))
            oFile.write(newLine)
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
            #newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", 0x" + str(hex(int(imm, 2)))[2:].zfill(4)
            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp(imm))
            oFile.write(newLine)

        else:                   # translate for addi
            rs = binary[6:11]
            rt = binary[11:16]
            imm = binary[16:32]

            # op rt, rs, imm
            #newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", 0x" + str(hex(int(imm, 2)))[2:].zfill(4)
            newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", " + str(getTwosComp(imm))
            oFile.write(newLine)

        word = ""
        binary = ""
        oFile.write("\n")
  #oFile.close()

def main():

    userResponse = input("Would like to begin Simulation? Enter yes or no: ")
    if (userResponse == "yes" or userResponse == "Yes"):
        Simulate()
    else:
        print("GoodBye")
if __name__== "__main__":
  main()
