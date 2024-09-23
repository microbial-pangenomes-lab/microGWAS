import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate zoomed-in Manhattan plots from GWAS results.")
    parser.add_argument("-i", "--input_file", required=True, help="Path to the mapped_all.tsv file.")
    parser.add_argument("-o", "--output_dir", required=True, help="Directory to save the output plots.")
    parser.add_argument("-r", "--reference_genome", required=True, help="Name of the reference genome to filter the data.")
    parser.add_argument("-p", "--patterns", required=True, help="Path to the patterns file for threshold calculation.")
    parser.add_argument("-z", "--zoom_regions", nargs=4, action='append', required=True, 
                        help="Zoom regions in format: name start_mb end_mb y_max. Can be specified multiple times for different regions.")
    parser.add_argument("-f", "--format", nargs='+', default=['png', 'svg'], choices=['png', 'svg', 'pdf', 'eps'], 
                        help="Output format(s) for the plots (default: png svg)")
    parser.add_argument("-d", "--dpi", type=int, default=300, help="DPI for raster formats like PNG (default: 300)")
    return parser.parse_args()

def calculate_threshold(patterns_file):
    """Calculate threshold using the external script."""
    try:
        threshold = float(subprocess.check_output([
            'python3', 'workflow/scripts/count_patterns.py', 
            '--threshold', patterns_file
        ]).decode().strip())
        print(f"Calculated threshold: {threshold}")
        return threshold
    except subprocess.CalledProcessError as e:
        print(f"Error calculating threshold: {e}")
        return 1e-5  # Default threshold 

def load_data(file_path, reference_genome):
    """Load and filter the GWAS results data."""
    df = pd.read_csv(file_path, sep="\t", usecols=['strain', 'start', 'end', 'lrt-pvalue', 'gene'])
    print(f"Total rows: {len(df)}")
    
    df = df[df['strain'] == reference_genome]
    print(f"Rows after filtering for {reference_genome}: {len(df)}")
    
    if len(df) == 0:
        print(f"No data found for strain: {reference_genome}")
        print("Available strains:")
        print(df['strain'].unique())
        return None
    
    df['pos'] = (df['start'] + df['end']) / (2 * 1_000_000)
    df['-log10(p-value)'] = -np.log10(df['lrt-pvalue'])
    return df

def plot_manhattan_zoom(data, x_range, y_max, title, output_prefix, threshold, formats, dpi):
    """Create a zoomed-in Manhattan plot."""
    fig, ax = plt.subplots(1, 1, figsize=(4, 2.5), constrained_layout=False)
    
    ax.plot(data['pos'], data['-log10(p-value)'], 'k.', alpha=0.3, rasterized=True)
    
    ax.axhline(-np.log10(threshold), color='r', ls='dashed', zorder=-1)
    
    ax.set_ylabel('$-log_{10}(pvalue)$')
    ax.set_xlabel('Genome position (Mb)')
    
    ax.text(0.05, 0.95, title, transform=ax.transAxes, va='top', ha='left', fontsize=10)
    
    ax.set_xlim(x_range)
    ax.set_ylim(-0.25, y_max)
    
    for fmt in formats:
        plt.savefig(f'{output_prefix}.{fmt}', dpi=dpi if fmt == 'png' else None, bbox_inches='tight', transparent=True)
    plt.close()

def main():
    args = parse_arguments()
    
    # Calculate threshold
    threshold = calculate_threshold(args.patterns)
    
    reference_data = load_data(args.input_file, args.reference_genome)
    
    if reference_data is None:
        print("Exiting due to no data found for the specified reference genome.")
        return
    
    print(f"Data range: {reference_data['pos'].min()} to {reference_data['pos'].max()} Mb")
    print(f"p-value range: {reference_data['lrt-pvalue'].min()} to {reference_data['lrt-pvalue'].max()}")
    
    for region in args.zoom_regions:
        name, start_mb, end_mb, y_max = region
        start_mb, end_mb, y_max = map(float, [start_mb, end_mb, y_max])
        
        output_path = f"{args.output_dir}/manhattan_zoom_{name}"
        plot_manhattan_zoom(reference_data, 
                            (start_mb, end_mb), 
                            y_max, 
                            name,  
                            output_path, 
                            threshold, 
                            args.format, 
                            args.dpi)
        print(f"Generated plot for region: {name}")
    
    print(f"All plots have been generated successfully in formats: {', '.join(args.format)}")

if __name__ == "__main__":
    main()