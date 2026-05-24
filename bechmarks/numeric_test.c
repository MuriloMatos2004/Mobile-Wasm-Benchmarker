#include <stdio.h>
#include <stdlib.h> // Needed for atoll (string to long long)

int main(int argc, char *argv[]) {
    // This takes the number from the command line
    if (argc < 2) {
        printf("Usage: ./test.wasm <number>\n");
        return 1;
    }

    long long input_size = atoll(argv[1]); 
    long long sum = 0;
    
    for (long long i = 0; i < input_size; i++) {
        sum += i;
    }
    
    printf("Result: %lld\n", sum);
    return 0;
}
