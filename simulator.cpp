#include <stdio.h>
#include <string.h>

#define MAXLINELENGTH 1000

int main(int argc, char *argv[]) {
    char line[MAXLINELENGTH];
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

    fclose(filePtr);

    return 0;
}
