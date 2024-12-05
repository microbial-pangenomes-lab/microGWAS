#!/usr/bin/env python


import sys
import argparse
import pandas as pd
from pysam import VariantFile


columns = ['Allele',
 'Annotation',
 'Annotation_Impact',
 'Gene_Name',
 'Gene_ID',
 'Feature_Type',
 'Feature_ID',
 'Transcript_BioType',
 'Rank',
 'HGVS.c',
 'HGVS.p',
 'cDNA.pos / cDNA.length',
 'CDS.pos / CDS.length',
 'AA.pos / AA.length',
 'Distance',
 'ERRORS / WARNINGS / INFO']


def get_options():
    description = 'Add ANN fields to a SNPs pyseer output'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('pyseer',
                        help='pyseer output')
    parser.add_argument('vcf',
                        help='vcf input')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    p = pd.read_csv(options.pyseer, sep='\t', index_col=0)

    vcf = VariantFile(options.vcf)
    res = []
    for v in vcf:
        idx = f'{v.chrom}_{int(v.pos)}_{v.ref}_{v.alts[0]}'
        if idx in p.index:
            for ann in v.info['ANN']:
                res.append([idx] + ann.split('|'))
    r = pd.DataFrame(res, columns=['variant'] + columns)
    r = r.set_index('variant')
    p.join(r, how='left').to_csv(sys.stdout, sep='\t')
