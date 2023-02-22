#!/usr/bin/env python


import os
import sys
import argparse
import numpy as np
import pandas as pd


def get_options():
    description = 'Make a summary of mapped unitigs'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('mapped',
                        help='Mapped unitigs table (all strains)')
    parser.add_argument('phenotypes',
                        help='Phenotypes table')
    parser.add_argument('phenotype',
                        help='Phenotype to use (column name; should be binary)')
    parser.add_argument('filtered',
                        help='Filtered variants table')

    parser.add_argument('--sort',
                        default='avg-lrt-pvalue',
                        help='Sort final table using this column (default: %(default)s)')
    parser.add_argument('--sort-descending',
                        default=True,
                        action='store_false',
                        help='Sort final table in descending order (default: false)')
    parser.add_argument('--unique',
                        default=False,
                        action='store_true',
                        help='Only look at uniquely-mapping unitigs (default: false)')
    parser.add_argument('--length',
                        type=int,
                        default=30,
                        help='Minimum unitig length (default: %(default)d)')
    parser.add_argument('--minimum-hits',
                        type=int,
                        default=1,
                        help='Minimum number of strains (default: %(default)d)')    
    parser.add_argument('--maximum-genes',
                        type=int,
                        default=10,
                        help='Maximum number of genes to which '
                             'a unitig can map to (default: %(default)d)')
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

    # read phenotypes
    p = pd.read_csv(options.phenotypes, sep='\t', index_col=0)
    p = p[options.phenotype]
    p.name = 'phenotype'
    # not checking if binary

    pangenome = {}
    if options.pangenome is not None:
        df = pd.read_csv(options.pangenome, sep='\t', index_col=0)
        df = df.T.sum() / df.shape[1]
        pangenome = df.to_dict()

    if options.pangenome_genes is not None:
        roary = pd.read_table(options.pangenome_genes,
                              sep=',',
                              low_memory=False)
        roary.set_index('Gene', inplace=True)
        # Drop the other info columns
        roary.drop(list(roary.columns[:2]), axis=1, inplace=True)

    gene_names = {}
    if options.reference is not None and options.gff_dir is not None:
        for strain in options.reference:
            for l in open(os.path.join(options.gff_dir, f'{strain}.gff'), 'r'):
                if 'CDS' not in l or 'gene=' not in l:
                    continue
                locus_tag = l.split('ID=')[1].split(';')[0]
                gene = l.split('gene=')[1].split(';')[0]
                gene_names[locus_tag] = gene

    m = pd.read_csv(options.mapped, sep='\t', index_col=0)
    # check empty
    if m.shape[0] == 0:
        sys.exit(0)
    # remove duplicated rows (?!)
    m = m.drop_duplicates(keep='first')
    #
    if options.unique:
        #singletons = m.groupby(['unitig', 'strain'])['start'].count().reset_index().groupby('unitig')['start'].max()
        singletons = m.groupby(['unitig', 'strain'])['start'].count()
        singletons = singletons[singletons <= 1]
        #m = m[m['unitig'].isin(singletons.index)]
        m = m[m['unitig'].isin({x[0] for x in singletons.index})]
    # remove unitigs that map to multiple genes across strains
    u = m.groupby('unitig')['gene'].nunique()
    m = m[m['unitig'].isin(u[u <= options.maximum_genes].index)]
    # remove short unitigs
    m['length'] = [len(x) for x in m['unitig'].values]
    m = m[m['length'] >= options.length]
    # check empty
    if m.shape[0] == 0:
        sys.exit(0)
    n = m.join(p.to_frame(), how='left').reset_index().rename(columns={'index':
        'strain'})

    n = n.groupby(['gene'])['strain'
                  ].nunique().reset_index().pivot_table(index='gene',
                                                        values='strain')
    n[np.isnan(n)] = 0
    n = n.rename(columns={'strain': 'strains'})

    f = pd.read_csv(options.filtered, sep='\t', index_col=0)
    # ugly hack
    #if 'lineage' not in f.columns:
    #    f.columns = ['af', 'filter-pvalue', 'lrt-pvalue', 'beta', 'lineage', 'notes']
    #
    v = m.reset_index().set_index('unitig').join(f, how='left')
    c = v.groupby('gene')[['af']].count().rename(columns={'af': 'unitigs'})
    if 'variant_h2' not in v.columns:
        v['variant_h2'] = np.nan
    v = v.groupby('gene')[['af', 'lrt-pvalue', 'beta', 'variant_h2']].mean()
    v = v.rename(columns={'af': 'avg-af',
                          'lrt-pvalue': 'avg-lrt-pvalue',
                          'beta': 'avg-beta'})

    a = n.join(v).join(c).sort_values('avg-lrt-pvalue')
    a = a[['strains', 'unitigs',
           'avg-af', 'avg-lrt-pvalue',
           'avg-beta', 'variant_h2']]
    # remove genes that are present in few strains total
    a = a[a['strains'] >= options.minimum_hits]
    # add pangenome info
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
