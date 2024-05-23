import argparse
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import numpy as np

def get_options():
    description = 'Manhattan plot'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('sample', help='Target mapped_all TSV file')
    return parser.parse_args()

def manhattan_plot(data):
    df = pd.read_csv(data, sep='\t', usecols=['strain', 'start', 'end', 'lrt-pvalue', 'gene'])
    df['pos'] = (df['start'] + df['end']) / (2 * 1_000_000)
    reference_strains = df['strain'].unique()
    t_output = subprocess.check_output(['python3','workflow/scripts/count_patterns.py','out/associations/phenotype/unitigs_patterns.txt'])
    t_output_lines = t_output.decode().split('\n')
    threshold_line = next(line for line in t_output_lines if 'Threshold:' in line)
    threshold_value = float(threshold_line.split('\t')[-1])

    for reference in reference_strains:
        reference_data = df[df['strain'] == reference]
        plt.figure(figsize=(10, 6))
        plt.rcParams['font.size'] = 14
        plt.scatter(reference_data['pos'], -np.log10(reference_data['lrt-pvalue']), color='grey', alpha=0.5)
        plt.axhline(-np.log10(threshold_value), color='red', linestyle='dashed')
        plt.xlabel('Genome Position')
        plt.ylabel('-log10(p-value)')
        plt.title(f'Manhattan Plot - {reference}')

        above_threshold = reference_data[reference_data['lrt-pvalue'] < threshold_value]
        labeled_positions = set()
        for i, row in above_threshold.iterrows():
            position = row['pos']
            gene_name = row['gene']
            if position not in labeled_positions:
                plt.annotate(gene_name, (position, -np.log10(row['lrt-pvalue'])), fontsize=8, ha='center')
                labeled_positions.add(position)
        plt.savefig('out/manhattan.png', dpi = 300)

if __name__ == "__main__":
    args = get_options()
    manhattan_plot(args.sample)

