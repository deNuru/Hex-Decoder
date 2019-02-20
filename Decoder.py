iFile = open("MIPS.txt", "r")
oFile = open("Assembly.txt.", "w")
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

## DONE: Create a table for all instruction opcodes (make a function like hex2bin perhaps?)
def getInstr(argument): 
    switcher = { 
        "001000": "addi",
        "101011": "sw",
        "100000": "add",
        "101010": "slt",
    } 
    return switcher.get(argument, "nothing") 

## DONE: Create a table for all instruction registers (make a function like hex2bin perhaps?)
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
        '13': "$t5",
        '14': "$t6",
        '15': "$t7",
        '16': "$s0",
        '17': "$s1",
        '18': "$s2",
        '19': "$s3",
        '20': "$s4",
        '21': "$s5",
        '22': "$s6",    
        '23': "$s7",
        '24': "$t8",
        '25': "$t9",
        '26': "$k0",
        '27': "$k1",
        '28': "$gp",
        '29': "$sp",
        '30': "$fp",
        '31': "$ra",
    } 
    return switcher.get(str(argument), "nothing") 

def getBin(number):
    switcher = {
        '0000' : "0",
        '0001' : "1",
        '0010' : "2",
        '0011' : "3",
        '0100' : "4",
        '0101' : "5",
        '0110' : "6",
        '0111' : "7",
        '1000' : "8",
        '1001' : "9",
        '1010' : "a",
        '1011' : "b",
        '1100' : "c",
        '1101' : "d",
        '1110' : "e",
        '1111' : "f"
    }
    return switcher.get(number)

for line in iFile:
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
        newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", 0x" + str(hex(int(imm, 2)))[2:].zfill(4)  + "(" + dec2regi(int(rs, 2)) + ")"
        oFile.write(newLine)
    else:                   # translate for addi
        rs = binary[6:11]
        rt = binary[11:16]
        imm = binary[16:32]

        # op rt, rs, imm
        newLine = getInstr(op) + " " + dec2regi(int(rt, 2)) + ", " + dec2regi(int(rs, 2)) + ", 0x" + str(hex(int(imm, 2)))[2:].zfill(4)
        oFile.write(newLine)

    word = ""
    binary = ""
    oFile.write("\n")

oFile.close()

