#!/usr/bin/env python3
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

INPUT_FILE = "results.csv"

def generate_charts():
    # Gather data points
    time_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    ram_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    try:
        with open(INPUT_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row['Category']
                size = int(row['Input_Size'])
                lang = row['Language']
                try:
                    time_data[cat][size][lang].append(float(row['Time_Seconds']))
                    ram_data[cat][size][lang].append(float(row['Max_RAM_KB']))
                except ValueError:
                    continue  # Gracefully skip any string allocation crashes
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    # Process each category (numeric, string, etc.) separately
    for cat in time_data.keys():
        sizes = sorted(time_data[cat].keys())
        
        # Calculate averages for plotting
        js_times = [sum(time_data[cat][s]['JavaScript'])/len(time_data[cat][s]['JavaScript']) if time_data[cat][s]['JavaScript'] else 0 for s in sizes]
        wasm_times = [sum(time_data[cat][s]['Wasm'])/len(time_data[cat][s]['Wasm']) if time_data[cat][s]['Wasm'] else 0 for s in sizes]
        
        js_rams = [sum(ram_data[cat][s]['JavaScript'])/len(ram_data[cat][s]['JavaScript']) if ram_data[cat][s]['JavaScript'] else 0 for s in sizes]
        wasm_rams = [sum(ram_data[cat][s]['Wasm'])/len(ram_data[cat][s]['Wasm']) if ram_data[cat][s]['Wasm'] else 0 for s in sizes]

        print(f"\n--- Speedup Factor Analysis for {cat.upper()} ---")
        for i, s in enumerate(sizes):
            j_t = js_times[i]
            w_t = wasm_times[i]
            if w_t > 0 and j_t > 0:
                speedup_S = j_t / w_t
                print(f"Scale 10^{len(str(s))-1}: WebAssembly is {speedup_S:.2f}x faster than JS (S = {speedup_S:.2f})")
            else:
                print(f"Scale 10^{len(str(s))-1}: Speedup calculation omitted (missing data or crash)")
        print("-" * 45)

        # Convert sizes to string labels for clean chart axis steps
        size_labels = [f"10^{len(str(s))-1}" for s in sizes]

        # --- CHART 1: EXECUTION LATENCY LINE GRAPH ---
        plt.figure(figsize=(7, 4.5))
        plt.plot(size_labels, js_times, marker='o', linewidth=2, color='#E15759', label='JavaScript (V8)')
        plt.plot(size_labels, wasm_times, marker='s', linewidth=2, color='#4E79A7', label='WebAssembly (Wasmtime)')
        
        plt.title(f'Execution Latency Scaling Trend: {cat.upper()}', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Workload Scale (Input Iterations)', fontsize=10, labelpad=10)
        plt.ylabel('Wall-Clock Execution Time (Seconds)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend(loc='upper left')
        plt.tight_layout()
        
        time_chart_name = f"chart_{cat.lower()}_time.png"
        plt.savefig(time_chart_name, dpi=300)
        plt.close()
        print(f"Saved execution time chart: {time_chart_name}")

        # --- CHART 2: MAXIMUM RAM CONSUMPTION BAR CHART ---
        plt.figure(figsize=(7, 4.5))
        x = range(len(sizes))
        width = 0.35

        plt.bar([i - width/2 for i in x], js_rams, width, label='JavaScript (V8)', color='#E15759', alpha=0.85)
        plt.bar([i + width/2 for i in x], wasm_rams, width, label='WebAssembly (Wasmtime)', color='#4E79A7', alpha=0.85)

        plt.title(f'Peak Memory Consumption Footprint: {cat.upper()}', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Workload Scale (Input Iterations)', fontsize=10, labelpad=10)
        plt.ylabel('Max Resident Set Size (KB)', fontsize=10)
        plt.xticks(x, size_labels)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.legend(loc='upper left')
        plt.tight_layout()

        ram_chart_name = f"chart_{cat.lower()}_ram.png"
        plt.savefig(ram_chart_name, dpi=300)
        plt.close()
        print(f"Saved memory allocation chart: {ram_chart_name}")

if __name__ == "__main__":
    generate_charts()
