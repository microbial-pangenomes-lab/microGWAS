#!/usr/bin/env python


import sys
import numpy as np
import pandas as pd


def get_options():
    import argparse

    description = 'Prepare a Manhattan plot'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('pyseer',
                        help='Unfiltered pyseer output')
    parser.add_argument('mapped',
                        help='Output of the map_back.py script')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    m = pd.read_csv(options.mapped, sep='\t')
    u = pd.read_csv(options.pyseer, sep='\t')

    j = m.set_index('unitig').join(u.set_index('variant'),
            how='inner').reset_index().rename(columns={'index':
                'unitig'})
    j = j[['strain', 'unitig'] + list(j.columns[2:])]
    j.to_csv(sys.stdout, sep='\t', index=False)
