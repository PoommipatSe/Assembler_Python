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