#include <stdio.h>
#include <string.h>

#define NUMMEMORY 65536 /* maximum number of words in memory */
#define NUMREGS 8 /* number of machine registers */
#define MAXLINELENGTH 1000

typedef struct stateStruct {
    int pc;
    int mem[NUMMEMORY];
    int reg[NUMREGS];
    int numMemory;
} stateType;

stateType init();
int retrieveBits(int , int, int);
stateType action(int, int, int, int, stateType);
void printReg(stateType);

int main(int argc, char *argv[]) {
    char line[MAXLINELENGTH];
    stateType state = init();
    FILE *filePtr;

    if (argc != 2) {
        printf("error: usage: %s <machine-code file>\n", argv[0]);
        return 0;
    }

    filePtr = fopen(argv[1], "r");
    if (filePtr == NULL) {
        printf("error: can't open file %s", argv[1]);
        perror("fopen");
        return 0;
    }

    for (state.numMemory = 0; fgets(line, MAXLINELENGTH, filePtr) != NULL; state.numMemory++) {
        if (sscanf(line, "%d", state.mem+state.numMemory) != 1) {
            printf("error in reading address %d\n", state.numMemory);
        } else {
            printf("memory[%d]=%d\n", state.numMemory, state.mem[state.numMemory]);
        }
    }

    int machineCode  = 8454151;
    int opCode = retrieveBits(24, 22, machineCode);
    int rs = retrieveBits(21, 19, machineCode);
    int rt = retrieveBits(18, 16, machineCode);

    state = action(opCode, rs, rt, machineCode, state);

    fclose(filePtr);

    return 0;
}

stateType init() {
    stateType state;
    state.pc = 0;
    memset(state.reg, 0, sizeof state.reg);
    state.numMemory = 0;
    return state;
}

int nthBit(int n, int regValue) {
    return (((1 << n) & regValue) >> n);
}

int retrieveBits(int most, int least, int regValue) {
    int num = 0;
    for (int len = 0; least <= most; ++least, ++len) {
        int bit = nthBit(least, regValue);
        num = (bit << len) | num; 
    }
    return num;
}

stateType add(int rs, int rt, int rd, stateType state) {
    state.reg[rd] = state.reg[rs] + state.reg[rt];
    state.pc += 1;
    return state;
}

stateType nand(int rs, int rt, int rd, stateType state) {
    state.reg[rd] =  ~(state.reg[rs] & state.reg[rt]);
    state.pc += 1;
    return state;
}

stateType rType(int opCode, int rs, int rt, int machineCode, stateType state) {
    int rd = retrieveBits(2, 0, machineCode);
    if (opCode == 0) {
        return add(rs, rt, rd, state);
    } else {
        return nand(rs, rt, rd, state);
    }
}

stateType load(int rs, int rt, int offset, stateType state) {
    state.reg[rt] = state.mem[state.reg[rs] + offset];
    state.pc += 1;
    return state;
}

stateType store(int rs, int rt, int offset, stateType state) {
    state.mem[state.reg[rs] + offset] = state.reg[rt];
    state.pc += 1;
    return state;
}

stateType iType(int opCode, int rs, int rt, int machineCode, stateType state) {
    int offset = retrieveBits(15, 0, machineCode);
    if (opCode == 2) {
        return load(rs, rt, offset, state);
    } else if (opCode == 3) {
        return store(rs, rt, offset, state);
    }
    return state;
}

stateType action(int opCode, int rs, int rt, int machineCode, stateType state) {
    if (opCode <= 1) {
        return rType(opCode, rs, rt, machineCode, state);
    } else if (opCode <= 4) {
        return iType(opCode, rs, rt, machineCode, state);
    }
}

void printReg(stateType state) {
    for(auto s : state.reg) {
        printf("%d ", s);
    }
    printf("\n");
}