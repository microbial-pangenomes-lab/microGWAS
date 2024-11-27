import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys


def get_options():
    description = 'Make a manhattan plot'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('sample', help='Target mapped_all TSV file')
    parser.add_argument('reference', help='Reference strain to use')
    parser.add_argument('output', help='Output file for the Manhattan plot')

    parser.add_argument('-z',
                        '--zoom', nargs=4,
                        default=None,
                        help='Produce a zoomed-in regions of the plot. '
                             'Format: name start_mb end_mb y_max. '
                             'start_mb and end_mb are expressed in Mbp, '
                             'y_max is the ceiling -log10(p-value) for the plot. '
                       )

    parser.add_argument('-t',
                        '--threshold',
                        default=None,
                        type=float,
                        help='Association p-value threshold (default: no threshold)'
                       )

    return parser.parse_args()


def manhattan_plot(data, threshold, reference, output, zoom):
    try:
        df = pd.read_csv(data, sep='\t', usecols=['strain', 'start', 'end',
                                                  'lrt-pvalue', 'gene'])
    except pd.errors.EmptyDataError:
        sys.stderr.write('Found an empty file so making an empty plot\n')
        open(output, 'w').close()
        sys.exit(0)
    except pd.errors.ParserError:
        sys.stderr.write('Could not parse input so making an empty plot\n')
        open(output, 'w').close()
        sys.exit(0)
    df['pos'] = (df['start'] + df['end']) / (2 * 1_000_000)
    df['-logpvalue'] = -np.log10(df['lrt-pvalue'])
    reference_strains = df['strain'].unique()

    reference_data = df[df['strain'] == reference]

    if zoom is None:
        plt.figure(figsize=(10, 6))
    else:
        # make the zoomed in plot a little smaller
        plt.figure(figsize=(8, 4.5))
        name, start, end, y_max = zoom
        start = float(start)
        end = float(end)
        y_max = float(y_max)

    plt.rcParams['font.size'] = 14
    plt.scatter(reference_data['pos'], reference_data['-logpvalue'],
                color='grey', alpha=0.5, rasterized=True)
    if threshold is not None:
        plt.axhline(-np.log10(threshold), color='red', linestyle='dashed')
    plt.xlabel('Genome Position (Mb)')
    plt.ylabel('$-log_{10}(pvalue)$')

    if zoom is not None:
        plt.xlim(start, end)
        plt.ylim(-0.25, y_max)
        plt.title(f'Manhattan Plot - {reference} - {name}')
    else:
        plt.title(f'Manhattan Plot - {reference}')

    plt.savefig(output, dpi=300)



if __name__ == "__main__":
    args = get_options()
    manhattan_plot(args.sample, args.threshold, args.reference, args.output,
                   args.zoom)

