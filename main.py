import re   #regex matching
fixzero = "0000000"

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

label_table = { #for label declaration

}


def filter_comment(a, op="//"): #eliminate comments ("//...")
    idx = a.find(op)
    if idx == -1:
        return a
    else:
        a = a[:idx]
    return a

if __name__ == '__main__':

    inputFile = open("test.txt", "r")


    # Prepare the input-file
    # -symbolic address (making a Dict for label declaration)
    # -exception handling (label duplication, undefine label, undefine opcode )
    line_count = 0
    for text in inputFile:

        text = filter_comment(text)
        word = text.split()

        if word[0] in inst_table:
            print("@Label"+text)
        else:
            if word[1] in inst_table:
                if re.match("^[a-zA-Z]{1,6}", word[0]):
                    if word[0] not in label_table:
                        #print(text + " ### has label : " + word[0] + " at address : ", line_count, "{0:b}".format(line_count))
                        label_table[word[0]] = line_count
                        print(text)
                    else:
                        raise ValueError("duplicate label")
                else:
                    raise ValueError("regex exception label")
            else:
                raise ValueError("undefine opcode")


        line_count += 1

    inputFile.close()

    print("prepare complete")


    '''
    inputFile = open("test.txt", "r")

    line_count = 0
    for text in inputFile:
        text = filter_comment(text)
        word = text.split()

        print(text)
        if word[0] in label_table:  #has label
            if word[1] == ".fill":
                if word[2] in label_table:  #stAddr .fill   start
                    machine_code = label_table[word[2]]
                elif word[2].lstrip("-").isdigit():     #five   .fill   5
                    machine_code = word[2]
                else:
                    raise ValueError("Undefine label")



        if word[0] in inst_table:   #no label
            if word[0] in {"sw", "lw", "beq"}:
                if word[3] in label_table and -32768 <= (label_table[word[3]]) << 32767:
                    offsetField = label_table[word[3]]
                    print( offsetField)

        line_count += 1

    inputFile.close()


    '''

