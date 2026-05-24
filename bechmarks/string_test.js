// string_test.js
const inputSize = parseInt(process.argv[2]);

if (isNaN(inputSize)) {
    console.log("Usage: node string_test.js <number>");
    process.exit(1);
}

// Dynamically allocate space and repeat a string pattern
// If inputSize is 100000, it creates a string of 100,000 'A's
let testString = "A".repeat(inputSize);

// Perform an operation on it to force the CPU/RAM to work
let stringLength = testString.length;

console.log(`Result: Processed string of length ${stringLength}`);
