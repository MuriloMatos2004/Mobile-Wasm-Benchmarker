// string_test.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <size>\n", argv[0]);
        return 1;
    }

    long long size = atoll(argv[1]);
    
    // Dynamically allocate memory based on the terminal argument
    char *str = (char *)malloc(size + 1);
    if (str == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Fill the memory to simulate data processing
    memset(str, 'A', size);
    str[size] = '\0'; // Null-terminator

    printf("Result: Processed memory buffer of size %lld bytes\n", size);
    
    free(str); // Clean up memory
    return 0;
}
