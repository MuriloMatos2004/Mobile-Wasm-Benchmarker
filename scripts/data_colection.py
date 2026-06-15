#!/usr/bin/env python3
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import statistics  # Added to compute standard deviation

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
        
        # --- CALCULATE MEANS AND STANDARD DEVIATIONS ---
        js_times_mean = []
        js_times_std = []
        wasm_times_mean = []
        wasm_times_std = []
        
        js_rams_mean = []
        js_rams_std = []
        wasm_rams_mean = []
        wasm_rams_std = []
        
        for s in sizes:
            # JavaScript Time Stats
            js_t_list = time_data[cat][s]['JavaScript']
            js_times_mean.append(statistics.mean(js_t_list) if js_t_list else 0)
            js_times_std.append(statistics.stdev(js_t_list) if len(js_t_list) > 1 else 0)
            
            # Wasm Time Stats
            wasm_t_list = time_data[cat][s]['Wasm']
            wasm_times_mean.append(statistics.mean(wasm_t_list) if wasm_t_list else 0)
            wasm_times_std.append(statistics.stdev(wasm_t_list) if len(wasm_t_list) > 1 else 0)
            
            # JavaScript RAM Stats
            js_r_list = ram_data[cat][s]['JavaScript']
            js_rams_mean.append(statistics.mean(js_r_list) if js_r_list else 0)
            js_rams_std.append(statistics.stdev(js_r_list) if len(js_r_list) > 1 else 0)
            
            # Wasm RAM Stats
            wasm_r_list = ram_data[cat][s]['Wasm']
            wasm_rams_mean.append(statistics.mean(wasm_r_list) if wasm_r_list else 0)
            wasm_rams_std.append(statistics.stdev(wasm_r_list) if len(wasm_r_list) > 1 else 0)

        print(f"\n--- Speedup Factor Analysis for {cat.upper()} ---")
        for i, s in enumerate(sizes):
            j_t = js_times_mean[i]
            w_t = wasm_times_mean[i]
            if w_t > 0 and j_t > 0:
                speedup_S = j_t / w_t
                print(f"Scale 10^{len(str(s))-1}: WebAssembly is {speedup_S:.2f}x faster than JS (S = {speedup_S:.2f})")
            else:
                print(f"Scale 10^{len(str(s))-1}: Speedup calculation omitted (missing data or crash)")
        print("-" * 45)

        # Convert sizes to string labels for clean chart axis steps
        size_labels = [f"10^{len(str(s))-1}" for s in sizes]

        # --- CHART 1: EXECUTION LATENCY LINE GRAPH WITH ERROR BARS ---
        plt.figure(figsize=(7, 4.5))
        
        # Using errorbar instead of plot to display standard deviation
        plt.errorbar(size_labels, js_times_mean, yerr=js_times_std, marker='o', linewidth=2, 
                     color='#E15759', label='JavaScript (V8)', capsize=4, elinewidth=1.5)
        plt.errorbar(size_labels, wasm_times_mean, yerr=wasm_times_std, marker='s', linewidth=2, 
                     color='#4E79A7', label='WebAssembly (Wasmtime)', capsize=4, elinewidth=1.5)
        
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

        # --- CHART 2: MAXIMUM RAM CONSUMPTION FOOTPRINT WITH ERROR BARS ---
        plt.figure(figsize=(7, 4.5))
        x = range(len(sizes))
        width = 0.35

        # Passing standard deviation directly into the yerr parameter of the bar charts
        plt.bar([i - width/2 for i in x], js_rams_mean, width, yerr=js_rams_std,
                label='JavaScript (V8)', color='#E15759', alpha=0.85, capsize=4, ecolor='#444444')
        plt.bar([i + width/2 for i in x], wasm_rams_mean, width, yerr=wasm_rams_std,
                label='WebAssembly (Wasmtime)', color='#4E79A7', alpha=0.85, capsize=4, ecolor='#444444')

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
