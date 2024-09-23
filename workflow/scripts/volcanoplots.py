import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import subprocess

plt.rcParams.update({'font.size': 16})  

parser = argparse.ArgumentParser(description="Create a volcano plot for significant genes.")
parser.add_argument("input_file", help="Path to the annotated summary file")
parser.add_argument("output_file", help="Path for the output file (without extension)")
parser.add_argument("--genes", nargs='+', help="List of genes to annotate and highlight")
parser.add_argument("-p", "--patterns", required=True, help="Path to the patterns file for threshold calculation.")
parser.add_argument("--format", choices=['png', 'svg', 'pdf'], default='png', help="Output file format (default: png)")
parser.add_argument("--dpi", type=int, default=300, help="DPI for the output image (default: 300)")

def calculate_threshold(patterns_file):
    """Calculate threshold using the external script."""
    try:
        threshold = float(subprocess.check_output([
            'python3', 'microGWAS/workflow/scripts/count_patterns.py', 
            '--threshold', patterns_file
        ]).decode().strip())
        print(f"Calculated threshold: {threshold}")
        return threshold
    except subprocess.CalledProcessError as e:
        print(f"Error calculating threshold: {e}")
        return 1e-5  

def create_volcano_plot(input_file, output_file, genes_to_annotate, p_value_threshold, output_format, dpi):
    
    data = pd.read_csv(input_file, sep="\t")

    data['-log10(p-value)'] = -np.log10(data['avg-lrt-pvalue'])

    plt.figure(figsize=(6, 6))

    plt.scatter(data['avg-beta'], data['-log10(p-value)'], color='indianred', s=50)

    plt.xlabel('Average Beta')
    plt.ylabel('-log10(p-value)')

    plt.axhline(-np.log10(p_value_threshold), color='red', linestyle='--')

    plt.axvline(0, color='black', linestyle='--')

    y_max = data['-log10(p-value)'].max()
    plt.ylim(0, y_max * 1.1) 

    x_min, x_max = data['avg-beta'].min(), data['avg-beta'].max()
    x_padding = (x_max - x_min) * 0.05 
    plt.xlim(x_min - x_padding, x_max + x_padding)

    if genes_to_annotate:
        for gene in genes_to_annotate:
            if gene in data['Preferred_name'].values:
                row = data[data['Preferred_name'] == gene].iloc[0]
                plt.annotate(gene, (row['avg-beta'], row['-log10(p-value)']),
                             xytext=(5, 5), textcoords='offset points', fontsize=14,
                             arrowprops=dict(arrowstyle='->', color='black'))

    plt.tight_layout()

    output_file_with_extension = f"{output_file}.{output_format}"
    plt.savefig(output_file_with_extension, format=output_format, dpi=dpi, bbox_inches='tight')
    print(f"Plot saved as {output_file_with_extension}")

if __name__ == "__main__":
    args = parser.parse_args()

    p_value_threshold = calculate_threshold(args.patterns)

    create_volcano_plot(args.input_file, args.output_file, args.genes, 
                        p_value_threshold, args.format, args.dpi)