#!/usr/bin/env python


import os
import sys
import argparse
import numpy as np
import pandas as pd
from limix.her import estimate


def load_covariates(infile, covariates, p):
    """Load and encode a covariates matrix
    Args:
        infile (str)
            Input file for the covariates matrix
        covariates (iterable or None)
            List of string indicating which columns to use and their
            interpretation. Example: `2q` indicates that the second column
            from the file is a quantitative variable, `2` indicates that
            that same column is categorical. If None, the matrix is loaded
            but nothing is done with it.
        p (pandas.Series)
            Phenotypes vector (n, 1)
    Returns:
        cov (pandas.DataFrame)
            Covariance matrix (n, m)

    NOTE: lifted from pyseer
    """
    c = pd.read_csv(infile,
                    index_col=0,
                    header=0,
                    sep='\t')
    c.index = c.index.astype(str)
    if np.any(c.index.duplicated()):
        sys.stderr.write('Covariate file contains duplicated sample names\n')
        sys.exit(1)

    if (len(p.index.difference(c.index)) > 0):
        sys.stderr.write("All samples with a phenotype must be present in covariate file\n")
        sys.exit(1)
    else:
        c = c.loc[p.index.intersection(c.index)]

    # which covariates to use?
    if covariates is None:
        cov = pd.DataFrame([])
    else:
        cov = []
        for col in covariates:
            cnum = int(col.rstrip('q'))
            if cnum == 1 or cnum > c.shape[1] + 1:
                sys.stderr.write('Covariates columns values should be '
                                 '> 1 and less than or equal to total number of ' +
                                 'columns (%d)\n' % (c.shape[1] + 1))
                return None
            if col[-1] == 'q':
                # quantitative
                cov.append(c.iloc[:,cnum-2])
            else:
                # categorical, dummy-encode it
                categories = set(c.iloc[:,cnum-2])
                categories.pop()
                for i, categ in enumerate(categories):
                    cov.append(pd.Series([1 if x == categ
                                          else 0
                                          for x in
                                          c.iloc[:,cnum-2].values],
                                         index=c.index,
                                         name=c.columns[cnum-2] + "_" + str(i)))
        if len(cov) > 0:
            cov = pd.concat(cov, axis=1)
        else:
            cov = pd.DataFrame([])
    return cov


def get_options():
    description = 'Estimate heritability'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('phenotypes',
                        help='Phenotypes and covariants file')
    parser.add_argument('similarities',
                        help='Similarity square matrix')

    parser.add_argument('-p', '--phenotype',
                        default='deces',
                        help='Phenotype to use (default: %(default)s)')
    parser.add_argument('--use-covariates',
                        default=None,
                        nargs='*',
                        help='Covariates to use. Format is "2 3q 4" '
                             '(q for quantitative) '
                             ' (default: load covariates but don\'t use '
                             'them)') 
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    p = pd.read_csv(options.phenotypes, sep='\t', index_col=0)
    samples = p.index

    s = pd.read_csv(options.similarities, sep='\t', index_col=0)
    s = s.loc[samples]

    p = p[options.phenotype]

    if options.use_covariates is not None:
        cov = load_covariates(options.phenotypes,
                              options.use_covariates,
                              p)
        cov['intercept'] = np.ones(cov.shape[0])
    else:
        cov = None

    print('phenotype\tlik\th2\th2_covariates')
    for lik in ['normal']:
        sys.stderr.write(f'Estimate heritability ({lik})\n')
        try:
            h2 = estimate(p, lik, s, None, verbose=False)
        except:
            sys.stderr.write(f'Failed estimation with {lik}!\n')
            h2 = ''
        if cov is not None:
            try:
                h2_cov = estimate(p, lik, s, cov, verbose=False)
            except:
                sys.stderr.write(f'Failed estimation with {lik} and covariates!\n')
                h2_cov = ''
        else:
            h2_cov = ''
        print(f'{options.phenotype}\t{lik}\t{h2}\t{h2_cov}')

