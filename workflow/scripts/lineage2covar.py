#!/usr/bin/env python


import sys
import argparse
import pandas as pd


def get_options():
    description = 'Compute variance/covariance matrix from lineages'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('lineages',
                        help='Lineage file (tab delimited, '
                             'sample -> lineage, no header)')
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    m = pd.read_csv(options.lineages, sep='\t', header=None)
    m.columns = ['strain', 'phylogroup']
    m = m.set_index('strain')
    for p in m['phylogroup'].unique():
        m[p] = [1 if m.loc[x, 'phylogroup'] == p
                else 0
                for x in m.index]
    m = m.drop(columns='phylogroup')
    m.T.cov().to_csv(sys.stdout, sep='\t')
