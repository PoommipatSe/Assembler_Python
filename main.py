import re   #import regex matching

fixedzero7 = "0000000" #reserve for 32-25th bits
fixedzero13 = "0000000000000"
fixedzero16 = "0000000000000000"
fixedzero22 = "0000000000000000000000"

inst_table = {  #instruction table
    "add"   :   "000",
    "nand"  :   "001",
    "lw"    :   "010",
    "sw"    :   "011",
    "beq"   :   "100",
    "jalr"  :   "101",
    "halt"  :   "110",
    "noop"  :   "111",
    ".fill" :   "xxx"

}

reg_table = {   #register table
    "0" :   "000",
    "1" :   "001",
    "2" :   "010",
    "3" :   "011",
    "4" :   "100",
    "5" :   "101",
    "6" :   "110",
    "7" :   "111",
}

label_table = { #for label declaration

}


def filter_comment(a, op="//"): #eliminate comments ("//...")
    idx = a.find(op)
    if idx == -1:
        return a
    else:
        a = a[:idx]
    return a

def file_prepare(filename1, filename2):

    inputFile = open(filename1, "r")
    processFile = open(filename2, "w")

    line_count = 0
    for text in inputFile:

        text = filter_comment(text)
        word = text.split()

        if word[0] in inst_table:
            temp_asm = "@Label"+text+"\n"
            print("@Label"+text)
            processFile.write(temp_asm)
        else:
            if word[1] in inst_table:
                if re.match("^[a-zA-Z]{1,6}", word[0]):
                    if word[0] not in label_table:
                        #print(text + " ### has label : " + word[0] + " at address : ", line_count, "{0:b}".format(line_count))
                        label_table[word[0]] = line_count
                        print(text)
                        processFile.write(text)
                    else:
                        raise ValueError("duplicate label")
                else:
                    raise ValueError("regex exception label")
            else:
                raise ValueError("undefine opcode")

        line_count += 1

    processFile.close()
    inputFile.close()

def file_assembling(filename2, filename3):

    processFile = open(filename2, "r")
    outputFile = open(filename3, "w")
    pc = 0  #tracking line which the program is working on
    for text in processFile:
        word = text.split()
        if len(word) == 0:  #skip the blank line
            continue
        print(word)

        if word[1] in ["add", "nand"]:  #R-type format (3 parameters)
            #zero(7) / opcode(3) / regA(3) / regB(3) / zero(13) / destReg(3)
            opcode = inst_table[word[1]]
            regA = reg_table[word[2]]
            regB = reg_table[word[3]]
            destReg = reg_table[word[4]]
            machine_code = str(int(fixedzero7+opcode+regA+regB+fixedzero13+destReg, 2))
            #print(machine_code)

        elif word[1] in ["sw", "lw", "beq"]:    #I-type format (3 parameters with offsetField)
            #zero(7) / opcode(3) / regA(3) / regB(3) / offsetField(16)
            opcode = inst_table[word[1]]
            regA = reg_table[word[2]]
            regB = reg_table[word[3]]

            if word[4] in label_table:  #checking if the offsetfield is a label or a number
                #if it is label, look up from label-table and calculate the jump range (adress label - (pc+1))
                offsetField_temp = int(label_table[word[4]]) - (pc+1)
            else:
                offsetField_temp = word[4]

            if int(offsetField_temp) < -32768 or int(offsetField_temp) > 32767:
                #checking offsetField range if it is between -32768 to 32767
                raise ValueError("offsetField is out of range")

            offsetField = format(int(offsetField_temp) % (1 << 16), '016b') #extend an integer to 2's complement 16-bits
            machine_code = str(int(fixedzero7+opcode+regA+regB+offsetField, 2))
            #print(machine_code)

        elif word[1] in ["jalr"]:   #J-type format (3 parameters with fixed-zero)
            #zero(7) / opcode(3) / regA(3) / regB(3) / zero(16)
            opcode = inst_table[word[1]]
            regA = reg_table[word[2]]
            regB = reg_table[word[3]]
            machine_code = str(int(fixedzero7+opcode+regA+regB+fixedzero16, 2))
            #print(machine_code)

        elif word[1] in ["halt", "noop"]:   #O-type format (0 parameter)
            #zero(7) / opcode(3) / zero(22)
            opcode = inst_table[word[1]]
            machine_code = str(int(fixedzero7+opcode+fixedzero22, 2))
            #print(machine_code)

        elif word[1] in [".fill"]:  #special format (1 parameter)
            if word[2] in label_table:
                machine_code = label_table[word[2]]
            else:
                machine_code = word[2]
            #print(machine_code)

        print(machine_code)
        outputFile.write(str(machine_code)+"\n")
        pc += 1

    processFile.close()
    outputFile.close()

if __name__ == '__main__':

    filename1 = "test.txt"          #assembly input file
    filename2 = "processFile.txt"   #processing file (the program works on this file)
    filename3 = "machine_code.txt"  #assembly output file

    # Prepare the input-file
    # -symbolic address (making a Dict for label declaration)
    # -exception handling (
    #   -label duplication,
    #   -undefine label,
    #   -undefine opcode)
    file_prepare(filename1, filename2)
    print("===================== file preparing is complete =======================")


    # translate aseembly code to machine language
    # -16-bits range checking
    # -2's complement 16-bits for I-type instructions is implemented
    file_assembling(filename2, filename3)
    print("===================== file assembling is complete =======================")




