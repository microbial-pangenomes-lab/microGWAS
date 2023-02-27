#!/usr/bin/env python

def get_options():
    import argparse

    description = 'Extract a representative from panaroo\'s orthologs'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('pangenome',
                        help='Panaroo\'s output (i.e. gene_presence_absence_roary.csv)')
    parser.add_argument('genes',
                        help='Panaroo\'s gene_data.csv file')
    
    parser.add_argument('--focus-strain',
                        default=None,
                        action='append',
                        help='Focus strain [Default: random strain]')
    parser.add_argument('--only-focus',
                        default=False,
                        action='store_true',
                        help='Only output OGs that are in the focus strain(s) '
                             '[Default: all or selected OGs]')
    parser.add_argument('--groups',
                        default=None,
                        help='OGs to focus on (tab-delimited summary file) '
                             '[Default: all of them]')
    parser.add_argument('--struct',
                        default=False,
                        action='store_true',
                        help='Tab-delimited summary file is a structural '
                             'variant file')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    import os
    import sys
    import csv
    import pandas as pd

    # Load roary
    roary = pd.read_csv(options.pangenome,
                        sep=',',
                        low_memory=False,
                        index_col=0)
    # Drop the other info columns
    roary.drop(list(roary.columns[:13]),
               axis=1,
               inplace=True)

    ogs = None
    if options.groups is not None:
        try:
            ogs = pd.read_csv(options.groups, sep='\t', index_col=0).index
            if options.struct:
                ogs = {y for x in set(ogs)
                       for y in x.split('-')}
            else:
                ogs = set(ogs)
        except:
            ogs = set()
        if len(ogs) == 0:
            sys.stderr.write(f'No OGs found\n')
            sys.exit(0)

    d = {}
    for g in roary.index:
        if ogs is not None and g not in ogs:
            continue
        genes = roary.loc[g].dropna()
        if options.focus_strain is None:
            genes = genes.sample(frac=1)
            strain = genes.index[0]
            gene = genes.values[0]
        else:
            gene = None
            for strain in options.focus_strain:
                if strain in genes.index:
                    gene = genes.loc[strain]
                    break
            if gene is None:
                if options.only_focus:
                    continue
                strain = genes.index[0]
                gene = genes.values[0]
        if ';' in gene:
            # pick first paralog
            sys.stderr.write(f'OG {g} has paralogs, picking the first one\n')
            gene = gene.split(';')[0]
        d[gene] = (strain, g)

    with open(options.genes) as csvfile:
        for row in csv.reader(csvfile, delimiter=','):
            gene_id = row[3]
            if gene_id not in d:
                continue
            protein = row[4]
            strain, og = d[gene_id]
            if '*' in protein:
                sys.stderr.write(f'Gene {gene_id} / {og} has a stop '
                                 f'codon in {strain}; skipping\n')
                continue
            print(f'>{og} {gene_id} {strain}')
            print(protein)
