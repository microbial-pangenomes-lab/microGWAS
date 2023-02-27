#!/usr/bin/env python


import os
import sys
import argparse
import numpy as np
import pandas as pd


categs = {'D': 'Cell cycle control, cell division, chromosome partitioning',
'M': 'Cell wall/membrane/envelope biogenesis',
'N': 'Cell motility',
'O': 'Post-translational modification, protein turnover, and chaperones',
'T': 'Signal transduction mechanisms',
'U': 'Intracellular trafficking, secretion, and vesicular transport',
'V': 'Defense mechanisms',
'W': 'Extracellular structures',
'Y': 'Nuclear structure',
'Z': 'Cytoskeleton',
'A': 'RNA processing and modification',
'B': 'Chromatin structure and dynamics',
'J': 'Translation, ribosomal structure and biogenesis',
'K': 'Transcription',
'L': 'Replication, recombination and repair',
'C': 'Energy production and conversion',
'E': 'Amino acid transport and metabolism',
'F': 'Nucleotide transport and metabolism',
'G': 'Carbohydrate transport and metabolism',
'H': 'Coenzyme transport and metabolism',
'I': 'Lipid transport and metabolism',
'P': 'Inorganic ion transport and metabolism',
'Q': 'Secondary metabolites biosynthesis, transport, and catabolism',
'R': 'General function prediction only',
'S': 'Function unknown',
'-': 'Not annotated'}


def get_options():
    description = 'Add annotations to a summary table'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('summary',
                        help='Summary table')
    parser.add_argument('annotations',
                        help='Output from eggnog mapper (*.emapper.annotations)')

    parser.add_argument('--no-summary',
                        default=False,
                        action="store_true",
                        help='Summary table is not really there')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    try:
        if not options.no_summary:
            # read summary
            s = pd.read_csv(options.summary, sep='\t', index_col=0)

        # read annotations
        a = pd.read_csv(options.annotations, sep='\t', skiprows=4,
                        skipfooter=3, index_col=0, engine='python')
    except:
        sys.exit(0)
    a['COG_name'] = [categs.get(x, '') for x in a['COG_category'].values]
    # keep only certain columns
    a = a[['COG_category', 'COG_name', 'Description', 'Preferred_name', 'GOs', 'EC', 'KEGG_ko',
           'KEGG_Pathway', 'KEGG_Module', 'KEGG_Reaction', 'KEGG_rclass', 'BRITE',
           'KEGG_TC', 'CAZy', 'BiGG_Reaction', 'PFAMs']]

    if not options.no_summary:
        a = s.join(a, how='left')
    a.to_csv(sys.stdout, sep='\t')
