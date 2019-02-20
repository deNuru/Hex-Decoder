myFile = open("hex.txt","r")
myOutputFile = open("output.txt", "w")
binary = ""
word = ""
newLine = ""



def hex(number):
    dic = {
        '0' : "0000",
        '1' : "0001",
        '2' : "0010",
        '3' : "0011",
        '4' : "0100",
        '5' : "0101",
        '6' : "0110",
        '7' : "0111",
        '8' : "1000",
        '9' : "1001",
        'a' : "1010",
        'b' : "1011",
        'c' : "1100",
        'd' : "1101",
        'e' : "1110",
        'f' : "1111"
    }
    return dic.get(number)


def getBin(number):
    dic = {
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
    return dic.get(number)


def getOp(number):
    dic = {
    '001000' : "addi",
    '100000' : "add",
    '100011' : "lw",
    '101011' : "sw",
    '101010' : "slt"
    }
    return dic.get(number)



def decToReg(number):
    dic = {
        0: "$0",
        1: "$1",
        2: "$2",
        3: "$3",
        4: "$4",
        5: "$5",
        6: "$6",
        7: "$7",
        8: "$8",
        9: "$9",
        10: "$10",
        11: "$11",
        12: "$12",
        13: "$t5",
        14: "$t6",
        15: "$t7",
        16: "$s0",
        17: "$s1",
        18: "$s2",
        19: "$s3",
        20: "$s4",
        21: "$s5",
        22: "$s6",
        23: "$s7",
        24: "$t8",
        25: "$t9",
        26: "$k0",
        27: "$k1",
        28: "$gp",
        29: "$sp",
        30: "$fp",
        31: "$ra",
    }
    return dic.get(number)



for line in myFile:
    word  = word + line[2:10]
    for bit in word:
        binary  = binary + str(hex(bit))
    op = binary[0:6]

    if (op == '001000'):
        rs = binary[6:11]
        rt = binary[11:16]
        imm = binary[16:32]
        a = imm
        i = ""
        o = 0
        p = 4
        for j in range(4):
            k = a[o:p]
            i = i + getBin(k)
            o = o + 4
            p = p + 4
        newLine = str(getOp(op)) + " " + decToReg(int(rt,2)) + "," + decToReg(int(rs,2)) + "," + "0x" + i
        myOutputFile.write(newLine)
        myOutputFile.write('\n')
        word = ""
        binary = ""

    elif (op == "100011" or op == "101011"):
         rs = binary[6:11]
         rt = binary[11:16]
         imm = binary[16:32]
         a = imm
         i = ""
         o = 0
         p = 4
         for j in range(4):
             k = a[o:p]
             i = i + getBin(k)
             o = o + 4
             p = p + 4
         newLine = str(getOp(op)) + " " + decToReg(int(rt,2)) + "," + "0x" + i + "(" + decToReg(int(rs,2)) + ")"
         myOutputFile.write(newLine)
         myOutputFile.write('\n')
         word = ""
         binary = ""

    elif (op == '000000'):
        rs = binary[6:11]
        rt = binary[11:16]
        dst = binary[16:21]
        function =  binary[26:32]
        newLine = str(getOp(function)) + " " + decToReg(int(dst,2)) + "," + decToReg(int(rs,2)) + "," +  decToReg(int(rt,2))
        myOutputFile.write(newLine)
        myOutputFile.write('\n')
        word = ""
        binary = ""
