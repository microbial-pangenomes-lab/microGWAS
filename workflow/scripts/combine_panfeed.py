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
    parser.add_argument('patterns',
                        help='hashes_to_patterns.tsv file from panfeed')

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

    n = k.join(p, how='inner')
    idx = set(n.index)

    # we need to also load the patterns table to add the "strain" column
    chunks = []
    for chunk in pd.read_csv(options.patterns, sep='\t',
                             index_col=0, chunksize=50000):
        keep = idx.intersection(chunk.index)
        if len(keep) > 0:
            chunks.append(chunk.loc[sorted(keep)])
    if len(chunks) == 0:
        sys.exit(0)
    h = pd.concat(chunks)
    h = h.unstack()
    h = h[h != 0]
    h = h.reset_index().rename(columns={'level_0': 'strain'})

    n.join(h.set_index('hashed_pattern')[['strain']],
           how='inner').to_csv(sys.stdout, sep='\t')
