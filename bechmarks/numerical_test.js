// numeric_test.js

// 1. Argument Parsing (Equivalent to argc checking)
// process.argv[0] is the node binary path
// process.argv[1] is the script file path (numeric_test.js)
// process.argv[2] is the first user argument (the number)
if (process.argv.length < 3) {
    console.log("Usage: node numeric_test.js <number>");
    process.exit(1);
}

// 2. Data Type Transformation (Equivalent to atoll)
// BigInt is required here because JavaScript standard numbers 
// lose precision above 9 quadrillion (the "Safe Integer" limit).
// BigInt forces 64-bit integer math, matching C's 'long long'.
const inputSize = BigInt(process.argv[2]);
let sum = 0n; // The 'n' suffix denotes a BigInt literal in JavaScript

// 3. The Computational Core (The Stress Test Loop)
for (let i = 0n; i < inputSize; i++) {
    sum += i;
}

// 4. Output and Exit
console.log(`Result: ${sum.toString()}`);
process.exit(0);
