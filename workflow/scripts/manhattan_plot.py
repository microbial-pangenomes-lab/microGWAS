import argparse
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import sys


def get_options():
    description = 'Make a manhattan plot'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('sample', help='Target mapped_all TSV file')
    parser.add_argument('patterns', help='Patterns file to derive a significance threshold')
    parser.add_argument('reference', help='Reference strain to use')
    parser.add_argument('output', help='Output file for the Manhattan plot')
    return parser.parse_args()


def manhattan_plot(data, patterns, reference, output):
    df = pd.read_csv(data, sep='\t', usecols=['strain', 'start', 'end',
                                              'lrt-pvalue', 'gene'])
    df['pos'] = (df['start'] + df['end']) / (2 * 1_000_000)
    reference_strains = df['strain'].unique()
    threshold = subprocess.check_output(['python3',
        'workflow/scripts/count_patterns.py', '--threshold',
        patterns])
    threshold = float(threshold)

    reference_data = df[df['strain'] == reference]
    plt.figure(figsize=(10, 6))
    plt.rcParams['font.size'] = 14
    plt.scatter(reference_data['pos'], -np.log10(reference_data['lrt-pvalue']), color='grey', alpha=0.5)
    plt.axhline(-np.log10(threshold), color='red', linestyle='dashed')
    plt.xlabel('Genome Position (Mb)')
    plt.ylabel('$-log_{10}(pvalue)$')
    plt.title(f'Manhattan Plot - {reference}')
    plt.savefig(output, dpi=300)


if __name__ == "__main__":
    args = get_options()
    manhattan_plot(args.sample, args.patterns, args.reference, args.output)

