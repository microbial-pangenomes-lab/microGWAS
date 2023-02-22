#!/usr/bin/env python


import sys
import argparse
import numpy as np
import pandas as pd


def get_options():
    description = 'Combine heritability estimates with CIs'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('variants',
                        help='Heritability estimates for variants')
    parser.add_argument('lineages',
                        help='Heritability estimates for lineages')
    parser.add_argument('ci',
                        help='Heritability CIs')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    hv = pd.read_csv(options.variants, sep='\t')
    hl = pd.read_csv(options.lineages, sep='\t')

    ci = pd.read_csv(options.ci, sep='\t')
    cis = {}
    for h2, cil, cih in ci.values:
        cis[h2] = cil, cih

    res = []
    for p, lik, h2, h2c in hv.values:
        h2 = round(h2, 5)
        res.append((p, 'variants', lik, 'naïve', h2,
            cis.get(h2, [np.nan, np.nan])[0],
            cis.get(h2, [np.nan, np.nan])[1],))
        if not np.isnan(h2c):
            h2c = round(h2c, 5)
            res.append((p, 'variants', lik, 'covariates', h2c,
                cis.get(h2c, [np.nan, np.nan])[0],
                cis.get(h2c, [np.nan, np.nan])[1],))
    for p, lik, h2, h2c in hl.values:
        h2 = round(h2, 5)
        res.append((p, 'lineages', lik, 'naïve', h2,
            cis.get(h2, [np.nan, np.nan])[0],
            cis.get(h2, [np.nan, np.nan])[1],))
        if not np.isnan(h2c):
            h2c = round(h2c, 5)
            res.append((p, 'lineages', lik, 'covariates', h2c,
                cis.get(h2c, [np.nan, np.nan])[0],
                cis.get(h2c, [np.nan, np.nan])[1],))

    r = pd.DataFrame(res, columns=['phenotype', 'genetics',
                                   'lik', 'analysis', 'h2',
                                   'h2_low', 'h2_high'])
    r.to_csv(sys.stdout, sep='\t', index=False)
