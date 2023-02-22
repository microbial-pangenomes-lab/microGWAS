#!/usr/bin/env python


import os
import sys
import argparse
import pandas as pd
from pysam import VariantFile
from Bio.SeqUtils import seq1


def get_options():
    description = 'Filter a VCF to return only deleterious variants'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('vcf',
                        help='vcf input')
    parser.add_argument('sift',
                        help='SIFT directory')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    s = None

    vcf = VariantFile(options.vcf)
    sys.stdout.write(str(vcf.header))
    for v in vcf:
        try:
            anns = v.info['ANN']
        except KeyError:
            # no annotation here, skip
            continue
        to_print = False
        for a in anns:
            a = a.split('|')
            kind = a[1]
            if 'disruptive' in kind:
                to_print = True
                break
            elif 'frameshift_variant' in kind:
                to_print = True
                break
            elif 'start_lost' in kind:
                to_print = True
                break
            elif 'stop_gained' in kind:
                to_print = True
                break
            elif 'stop_lost' in kind:
                to_print = True
                break
            elif 'missense_variant' in kind:
                gene = a[3]
                prot = a[10]
                if s is None or s[0] != gene:
                    try:
                        m = pd.read_csv(os.path.join(options.sift,
                                                     f'{gene}.tsv'),
                                        sep='\t')
                        s = (gene, m)
                    except FileNotFoundError:
                        continue
               
                # corner case
                if '_' in prot:
                    continue
                
                pos = prot[2:]
                # Get start position
                i = 0
                while True:
                    i += 1
                    pos = pos[1:-1]
                    try:
                        int(pos)
                        break
                    except:
                        if pos.strip() == '':
                            break
                        continue
                if pos.strip() == '':
                    continue
                
                # multiple Aa substitutions in one go?
                muts = []
                j = 0
                k = 0
                prot = prot[2:]
                while j < i:
                    wt_aa = prot[j:j+3]
                    mut_aa = prot[i+len(pos)+j:i+len(pos)+3+j]
                    pos_aa = int(pos)+k
                    muts.append( (seq1(wt_aa), pos_aa, seq1(mut_aa)) )
                    j += 3
                    k += 1

                for wt_aa, pos_aa, mut_aa in muts:
                    # avoid synonymous mutations
                    if wt_aa == mut_aa:
                        continue
                    m = s[1]
                    try:
                        entry = m[(m['pos'] == pos_aa) &
                                  (m['ref'] == wt_aa) &
                                  (m['alt'] == mut_aa) &
                                  (m['median_ic'] < 3.25)].iloc[0]
                    except IndexError:
                        # no score, ignore
                        continue
                    if entry['score'] <= 0.05:
                        to_print = True
                        break
        
        if to_print:
            sys.stdout.write(str(v))
