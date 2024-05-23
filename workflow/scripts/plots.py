import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def get_options():
    description = 'Make plots to visualize enrichment analysis'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('cog', help='COG.tsv from enrichment analysis')
    parser.add_argument('cog_plot', help='Output plot for COG enrichment analysis')
    parser.add_argument('go', help='GO.tsv from GO term analysis')
    parser.add_argument('go_plot', help='Output plot for GO term analysis')
    parser.add_argument('kegg', help='KEGG.tsv from KEGG enrichment analysis')
    parser.add_argument('kegg_plot', help='Output plot for KEGG enrichment analysis')

    return parser.parse_args()

def plot_enrichment(data, plot_file, category_label):
    try:
        enrichment_data = pd.read_csv(data, sep='\t')
        if enrichment_data.empty:
            sys.exit(f"Error: {data} file is empty.")
    except FileNotFoundError:
        sys.exit(f"Error: {data} file not found.")

    enrichment_data['gene_count'] = enrichment_data['genes'].apply(len)
    enrichment_data['empirical-qvalue'] = enrichment_data['empirical-qvalue'].fillna(1)
    enrichment_data_sorted = enrichment_data.sort_values(by='gene_count', ascending=True)
    enrichment_data_sorted['-log10(padj)'] = -np.log10(enrichment_data_sorted['empirical-qvalue'])

    # Plotting
    plt.figure(figsize=(6, 8))
    bars = plt.barh(enrichment_data_sorted['category'], enrichment_data_sorted['gene_count'],
                    color=plt.cm.viridis(enrichment_data_sorted['-log10(padj)'] / max(enrichment_data_sorted['-log10(padj)'])))

    plt.xlabel('Gene Count')
    plt.ylabel(category_label)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='viridis',
                                               norm=plt.Normalize(vmin=enrichment_data_sorted['-log10(padj)'].min(),
                                                                  vmax=enrichment_data_sorted['-log10(padj)'].max())),
                        pad=0.05, shrink=0.5)
    cbar.set_label('padj')

    plt.savefig(plot_file, dpi=300)
    plt.close()

def main():
    options = get_options()

    # Plot COG data
    plot_enrichment(options.cog, options.cog_plot, 'COG Category')

    # Plot GO data
    plot_enrichment(options.go, options.go_plot, 'GO Category')

    # Plot KEGG data
    plot_enrichment(options.kegg, options.kegg_plot, 'KEGG Category')

if __name__ == "__main__":
    main()
