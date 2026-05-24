#!/bin/bash

# 1. Establish the output spreadsheet destination
OUTPUT_FILE="results.csv"

# 2. Write the CSV headers (Crucial so you know what the columns mean)
echo "Language,Category,Input_Size,Run,Time_Seconds,Max_RAM_KB" > $OUTPUT_FILE

# 3. Define the complete experimental parameters (2 x 3 x 3 = 18 experiments * 2 languages = 36 runs)
CATEGORIES=("numeric" "string") 
SIZES=("100000" "10000000" "1000000000") 
REPEATS=(1 2 3) 

echo "Starting Thesis Benchmark Pipeline..."
echo "------------------------------------"

for cat in "${CATEGORIES[@]}"; do
    for size in "${SIZES[@]}"; do
        for run in "${REPEATS[@]}"; do

            # --- PROCESS 1: WEBASSEMBLY EXECUTION & CAPTURE ---
            echo "Running WASM | Category: $cat | Size: $size | Run: $run"
            
            # Execute, isolate metrics, and store in a variable
            WASM_METRICS=$(/usr/bin/time -f "%e,%M" wasmtime "${cat}_test.wasm" $size 2>&1 >/dev/null)
            
            # SAVE TO CSV: Append the data to your file
            echo "Wasm,$cat,$size,$run,$WASM_METRICS" >> $OUTPUT_FILE


            # --- PROCESS 2: JAVASCRIPT EXECUTION & CAPTURE ---
            echo "Running JS   | Category: $cat | Size: $size | Run: $run"
            
            # Execute, isolate metrics, and store in a variable
            JS_METRICS=$(/usr/bin/time -f "%e,%M" node "${cat}_test.js" $size 2>&1 >/dev/null)
            
            # SAVE TO CSV: Append the data to your file
            echo "JavaScript,$cat,$size,$run,$JS_METRICS" >> $OUTPUT_FILE

        done
    done
done

echo "------------------------------------"
echo "Benchmark Complete! 36 runs processed. Data secured in $OUTPUT_FILE"
