import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def get_options():
    description = 'Make plots from COG analysis'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('cog',
                        help='COG.tsv from functional enrichment analysis')
    parser.add_argument('cog_plot',
                        help='Output plot for functional enrichment analysis')

    return parser.parse_args()

def main():
    options = get_options()

    # Read COG data
    try:
        cog_data = pd.read_csv(options.cog, sep='\t')
        if cog_data.empty:
            sys.exit("Error: COG.tsv file is empty.")
    except FileNotFoundError:
        sys.exit("Error: COG.tsv file not found.")

    # Sort COG data by gene count
    cog_data['gene_count'] = cog_data['genes'].apply(len)
    cog_data['empirical-qvalue'] = cog_data['empirical-qvalue'].fillna(1)
    cog_data_sorted = cog_data.sort_values(by='gene_count', ascending=True)
    cog_data_sorted['-log10(padj)'] = -np.log10(cog_data_sorted['empirical-qvalue'])

    # Plot COG data
    plt.figure(figsize=(6, 8))
    bars = plt.barh(cog_data_sorted['category'], cog_data_sorted['gene_count'], 
                    color=plt.cm.viridis(cog_data_sorted['-log10(padj)'] / max(cog_data_sorted['-log10(padj)'])))

    plt.xlabel('Gene Count')
    plt.ylabel('COG Category')

    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='viridis', 
                                               norm=plt.Normalize(vmin=cog_data_sorted['-log10(padj)'].min(), 
                                                                  vmax=cog_data_sorted['-log10(padj)'].max())), 
                        pad=0.05, shrink=0.5)
    cbar.set_label('padj')

    plt.savefig(options.cog_plot, dpi=300)
    plt.close()

if __name__ == "__main__":
    main()

