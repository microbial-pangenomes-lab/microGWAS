#!/usr/bin/env python


import sys
import gzip
import math
import random
import argparse
import numpy as np
import pandas as pd


def get_options():
    description = 'Compute variance/covariance matrix from all unitigs'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('phenotypes',
                        help='Phenotypes file (tab delimited, with header, '
                              first column indicates strain names, '
                              used to compute AF)')
    parser.add_argument('unitigs',
                        help='Unitigs txt file')

    parser.add_argument('--sample',
                        type=float,
                        default=1,
                        help='What fraction of unitigs to sample (default: %(default).2f)')
    parser.add_argument('--compressed',
                        action='store_true',
                        default=False,
                        help='Unitigs file is gzipped')
    parser.add_argument('--max-af',
                        type=float,
                        default=1,
                        help='Maximum unitig frequency (included, default: %(default).2f')
    parser.add_argument('--min-af',
                        type=float,
                        default=0,
                        help='Minimum unitig frequency (included, default: %(default).2f')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    m = pd.read_csv(options.phenotypes, sep='\t', index_col=0)
    idx = set(m.index)
    all_vars = []
    i = 0
    j = 0

    if options.compressed:
        handle = gzip.open(options.unitigs)
    else:
        handle = open(options.unitigs)

    for line_in in handle:
        if options.compressed:
            line_in = line_in.decode()
        var_name, strains = (line_in.split()[0],
                             line_in.rstrip().split('|')[1].lstrip().split())
        strains = {x.split(':')[0] for x in strains}
        correct = math.sqrt(len(var_name))
        d = {x: 1 / correct
             for x in strains
             if x in idx}
        for x in idx:
            if x not in d:
                d[x] = 0
        af = sum(d.values()) / len(idx)
        if af > options.max_af or af < options.min_af:
            continue
        j += 1
        if options.sample < 1 and random.random() > options.sample:
            continue
        i += 1
        all_vars.append(pd.DataFrame([d[x] for x in idx if x in d],
                                  columns=[i],
                                  index=idx).T)
        if not i % 1000:
            sys.stderr.write(f'read {i} unitigs ({j} eligible)\n')
    m = pd.concat(all_vars)
    del all_vars
        
    m.cov().to_csv(sys.stdout, sep='\t')
