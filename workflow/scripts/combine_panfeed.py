#!/usr/bin/env python


import sys
import argparse
import numpy as np
import pandas as pd


def get_options():
    description = 'Prepare the input for mapped_summary.py for panfeed'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('pyseer',
                        help='Pyseer results for panfeed '
                             '(the first column should contain the hashes)')
    parser.add_argument('kmers',
                        help='kmers_to_hashes.tsv file from panfeed')

    parser.add_argument('--threshold',
                        type=float,
                        default=1,
                        help='p-value threshold (default: %(default).2f)')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    p = pd.read_csv(options.pyseer, sep='\t', index_col=0)
    p = p[p['lrt-pvalue'] <= options.threshold].copy()

    k = pd.read_csv(options.kmers, sep='\t', index_col=2)

    k.join(p, how='inner').to_csv(sys.stdout, sep='\t')
