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

def plot_enrichment(data, plot_file, category_label, count_col,
                    qval_col, name_cols):
    try:
        enrichment_data = pd.read_csv(data, sep='\t')
    except FileNotFoundError:
        sys.exit(f"Error: {data} file not found.")
    except pd.errors.EmptyDataError:
        open(plot_file, 'w').close()
        return

    enrichment_data[qval_col] = enrichment_data[qval_col].fillna(1)
    enrichment_data_sorted = enrichment_data.sort_values(by=count_col, ascending=True)
    enrichment_data_sorted['-log10(padj)'] = -np.log10(enrichment_data_sorted[qval_col])

    height = max([8, enrichment_data_sorted.shape[0] / 6])
    plt.figure(figsize=(6, height))
    bars = plt.barh([' - '.join(x).rstrip() for x in enrichment_data_sorted[name_cols].values],
                    enrichment_data_sorted[count_col],
                    color=plt.cm.viridis(enrichment_data_sorted['-log10(padj)'] / max(enrichment_data_sorted['-log10(padj)'])))

    plt.xlabel('Gene Count')
    plt.ylabel(category_label)
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap='viridis',
                               norm=plt.Normalize(vmin=enrichment_data_sorted['-log10(padj)'].min(),
                               vmax=enrichment_data_sorted['-log10(padj)'].max())),
                        pad=0.05, shrink=0.5,
                        ax=plt.gca()
                        )
    cbar.set_label('$-log_{10}(pvalue)$')

    plt.xscale('log')

    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    options = get_options()

    # Plot COG data
    plot_enrichment(options.cog, options.cog_plot, 'COG category',
                    'gene_count', 'empirical-qvalue', ['cog', 'category'])

    # Plot GO data
    plot_enrichment(options.go, options.go_plot, 'GO term',
                    'study_count', 'p_fdr_bh', ['GO', 'name'])

    # Plot KEGG data
    plot_enrichment(options.kegg, options.kegg_plot, 'KEGG pathway',
                    'gene_count', 'qvalue', ['KEGG_pathway'])

if __name__ == "__main__":
    main()
