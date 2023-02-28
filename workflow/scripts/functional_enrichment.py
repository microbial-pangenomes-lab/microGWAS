#!/usr/bin/env python


cogs = 'ABCDEFGHIJKLMNOPQRSTUYZ'

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
'X': 'Not annotated'}


def get_options():
    import argparse

    description = 'FUnctional enrichment analysis'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('sample',
                        help='Target annotated summary table')
    parser.add_argument('reference',
                        help='Reference annotated table')
    parser.add_argument('obo',
                        help='Gene ontology obo file')
    parser.add_argument('cog',
                        help='COG enrichment output')
    parser.add_argument('go',
                        help='GO enrichment output')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    import sys
    import numpy as np
    import pandas as pd
    from scipy import stats
    import statsmodels.api as sm
    from goatools.obo_parser import GODag
    from goatools.goea.go_enrichment_ns import GOEnrichmentStudy

    m = pd.read_csv(options.reference, sep='\t')
    m.loc[m.index.difference(m['COG_category'].dropna().index),
          'COG_category'] = 'X'

    try:
        n = pd.read_csv(options.sample, sep='\t')
    except:
        # most likely empty file
        f = open(options.cog, 'w')
        f.close()
        f = open(options.go, 'w')
        f.close()
        sys.exit(0)
    n.loc[n.index.difference(n['COG_category'].dropna().index),
          'COG_category'] = 'X'

    res = []
    for cog in cogs + 'X':
        pop_c = m[m['COG_category'].str.contains(cog)].shape[0]
        pop_n = m[~m['COG_category'].str.contains(cog)].shape[0]

        study_c = n[n['COG_category'].str.contains(cog)].shape[0]
        study_n = n[~n['COG_category'].str.contains(cog)].shape[0]

        table = [[study_c, pop_c],
                 [study_n, pop_n]]
        odds_ratio, pvalue = stats.fisher_exact(table, alternative='greater')
            
        # empirical
        ratios = []
        for _ in range(100):
            pop_c = m[m['COG_category'].str.contains(cog)].shape[0]
            pop_n = m[~m['COG_category'].str.contains(cog)].shape[0]
            
            r = m.sample(n.shape[0])
            study_r_c = r[r['COG_category'].str.contains(cog)].shape[0]
            study_r_n = r[~r['COG_category'].str.contains(cog)].shape[0]
            
            table = [[study_r_c, pop_c],
                     [study_r_n, pop_n]]
            ratios.append(stats.fisher_exact(table, alternative='greater')[0])

        zscores = stats.zscore(ratios + [odds_ratio])
        pvalues = stats.norm.sf(abs(zscores))
        qvalues = sm.stats.multipletests(pvalues, alpha=0.05, method='fdr_bh')[1]
        
        res.append((cog, categs[cog], pvalue, qvalues[-1]))

    r = pd.DataFrame(res,
                     columns=['cog', 'category', 'pvalue', 'empirical-qvalue'])

    r['qvalue'] = sm.stats.multipletests(r['pvalue'], alpha=0.05, method='fdr_bh')[1]
    r = r[['cog', 'category', 'pvalue', 'qvalue', 'empirical-qvalue']]

    r.to_csv(options.cog, sep='\t', index=False)

    obodag = GODag(options.obo)

    assoc = {k: {y for y in v.split(',')}
             for k, v in m.set_index(m.columns[0])['GOs'].dropna().to_dict().items()}
    for k, v in n.set_index(n.columns[0])['GOs'].dropna().to_dict().items():
        if k in assoc:
            continue
        assoc[k] = {y for y in v.split(',')}

    go = GOEnrichmentStudy(assoc.keys(), assoc, obodag, methods=['fdr_bh'])
    res = go.run_study(set(n[n.columns[0]]))

    passing = [x for x in res
               if x.get_pvalue() < 0.05]

    res = []
    for go in passing:
        if go.depth < 3:
            continue
        go.study_items = [x for x in go.study_items]
        res.append(str(go).split('\t'))
    if len(res) > 0:
        r = pd.DataFrame(res,
                         columns=go.get_prtflds_default())

        r.to_csv(options.go, sep='\t', index=False)
    else:
        f = open(options.go, 'w')
        f.close()
