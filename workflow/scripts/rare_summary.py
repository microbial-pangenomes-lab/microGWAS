#!/usr/bin/env python


import os
import sys
import argparse
import numpy as np
import pandas as pd


def get_options():
    description = 'Make a summary of burden tests results'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('rare',
                        help='Burden test results table')
    parser.add_argument('mainreference',
                        help='Reference genome used for burden test')

    parser.add_argument('--sort',
                        default='lrt-pvalue',
                        help='Sort final table using this column (default: %(default)s)')
    parser.add_argument('--sort-descending',
                        default=True,
                        action='store_false',
                        help='Sort final table in descending order (default: false)')
    parser.add_argument('--pangenome',
                        default=None,
                        help='Panaroo Rtab output '
                             'to single out core genes (default: do not provide this)')
    parser.add_argument('--pangenome-genes',
                        default=None,
                        help='Panaroo CSV output '
                             'to map to references (default: do not provide this)')
    parser.add_argument('--reference',
                        default=None,
                        action='append',
                        help='Reference genome '
                             'to report reference genes (default: do not provide this)')
    parser.add_argument('--gff-dir',
                        default=None,
                        help='GFF directory '
                             'to report gene names for reference genes (default: do not provide this)')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    pangenome = {}
    if options.pangenome is not None:
        df = pd.read_csv(options.pangenome, sep='\t', index_col=0)
        df = df.T.sum() / df.shape[1]
        pangenome = df.to_dict()

    mainreference = {}
    if options.pangenome_genes is not None:
        roary = pd.read_table(options.pangenome_genes,
                              sep=',',
                              low_memory=False)
        roary.set_index('Gene', inplace=True)
        # Drop the other info columns
        roary.drop(list(roary.columns[:2]), axis=1, inplace=True)
        roary = roary[sorted(set([options.mainreference,]).union(options.reference))]
        for k, v in roary[options.mainreference].items():
            if str(v) == 'nan':
                continue
            for locus in v.split(';'):
                mainreference[locus] = k

    gene_names = {}
    if options.reference is not None and options.gff_dir is not None:
        for strain in options.reference:
            for l in open(os.path.join(options.gff_dir, f'{strain}.gff'), 'r'):
                if 'CDS' not in l or 'gene=' not in l:
                    continue
                locus_tag = l.split('ID=')[1].split(';')[0]
                gene = l.split('gene=')[1].split(';')[0]
                gene_names[locus_tag] = gene

    a = pd.read_csv(options.rare, sep='\t', index_col=0)
    # check empty
    if a.shape[0] == 0:
        sys.exit(0)
    # add pangenome info
    a.index = [mainreference.get(x, x)
               for x in a.index]
    a['pangenome-frequency'] = [pangenome.get(x, np.nan)
                      for x in a.index]
    a['pangenome-category'] = np.nan
    a.loc[a[a['pangenome-frequency'] >= 0.99].index,
          'pangenome-category'] = 'core'
    a.loc[a[(a['pangenome-frequency'] < 0.99) &
            (a['pangenome-frequency'] >= 0.95)].index,
          'pangenome-category'] = 'soft-core'
    a.loc[a[(a['pangenome-frequency'] < 0.95) &
            (a['pangenome-frequency'] >= 0.15)].index,
          'pangenome-category'] = 'shell'
    a.loc[a[a['pangenome-frequency'] < 0.15].index,
          'pangenome-category'] = 'cloud'
    # add references info
    for strain in options.reference:
        a[strain] = [roary.loc[x, strain] if x in roary.index
                     else np.nan
                     for x in a.index]
        if options.gff_dir is not None:
            a[f'{strain}-name'] = [';'.join([gene_names.get(y, '')
                                             for y in x.split(';')])
                                   if str(x) != 'nan'
                                   else ''
                                   for x in a[strain].values]
    #
    a = a.sort_values(options.sort, ascending=options.sort_descending)
    a.to_csv(sys.stdout, sep='\t')
