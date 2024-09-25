import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})

def get_options():
    parser = argparse.ArgumentParser(
            description="Create a volcano plot for significant genes")

    parser.add_argument("annotated_summary",
                        help="Path to the annotated summary file")
    parser.add_argument("output_file", help="Path for the output figure")

    parser.add_argument("--genes", nargs='+',
            help="List of genes to annotate and highlight")

    parser.add_argument('-t',
                        '--threshold',
                        default=None,
                        type=float,
                        help='Association p-value threshold (default: no threshold)'
                       )

    return parser.parse_args()


def create_volcano_plot(input_file, output_file, genes_to_annotate,
                        p_value_threshold):

    data = pd.read_csv(input_file, sep="\t")

    y_col = 'avg-lrt-pvalue'
    if y_col not in data.columns:
        y_col = 'lrt-pvalue'
    x_col = 'avg-beta'
    if x_col not in data.columns:
        x_col = 'beta'

    data['-log10(p-value)'] = -np.log10(data[y_col])

    plt.figure(figsize=(6, 6))

    plt.scatter(data[x_col], data['-log10(p-value)'],
                color='grey', alpha=0.7, s=50)

    plt.xlabel('Beta')
    plt.ylabel('$-log_{10}(pvalue)$')

    if p_value_threshold is not None:
        plt.axhline(-np.log10(p_value_threshold), color='red',
                    linestyle='--')

    plt.axvline(0, color='black', linestyle='--')

    y_max = data['-log10(p-value)'].max()
    plt.ylim(0, y_max * 1.1)

    x_min, x_max = data[x_col].min(), data[x_col].max()
    x_padding = (x_max - x_min) * 0.1
    plt.xlim(x_min - x_padding, x_max + x_padding)

    if genes_to_annotate:
        for gene in genes_to_annotate:
            if gene in data['Preferred_name'].values:
                row = data[data['Preferred_name'] == gene].iloc[0]
                plt.annotate(gene, (row[x_col], row['-log10(p-value)']),
                             xytext=(5, 5), textcoords='offset points',
                             arrowprops=dict(arrowstyle='->', color='black'))
            else:
                print(f'Can\'t find {gene}, will not annotate')

    plt.tight_layout()

    plt.savefig(output_file, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    args = get_options()

    create_volcano_plot(args.annotated_summary, args.output_file, args.genes,
                        args.threshold)
