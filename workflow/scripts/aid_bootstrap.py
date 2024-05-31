#!/usr/bin/env python

def get_options():
    import argparse

    # create the top-level parser
    description = "Check which samples are to be used in the GWAS pipeline"
    parser = argparse.ArgumentParser(description = description)

    parser.add_argument('data', action='store',
                        help='Data input file (first column is sample names, '
                             'a column named "gff" and one named "fasta" should '
                             'be present, each indicating the absolute or relative path '
                             'to the annotations and assemblies. It is assumed '
                             'that all file names are in the form SAMPLE[.gff,.fasta])')
    parser.add_argument('--out', action='store',
                        default='out',
                        help='Output directory in which to write the output files '
                             '(default: %(default)s)')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    import os
    import sys
    import pandas as pd

    m = pd.read_csv(options.data, sep='\t', index_col=0)
    if 'gff' not in m.columns and 'fasta' not in m.columns:
        sys.stderr.write('Input data file must contain a "gff" and a "fasta" column\n')
        sys.exit(1)

    found = set()
    missing = set()
    name = set()
    for sample, row in m.iterrows():
        gff = row['gff']
        fasta = row['fasta']

        # check that the file names follow the SAMPLE.EXT convention
        # if not it would break panaroo and panfeed
        if '.'.join(os.path.split(gff)[-1].split('.')[:-1]) != sample:
            sys.stderr.write(f'GFF file name not matching sample name ({sample}, {gff})')
            name.add(sample)
        if '.'.join(os.path.split(fasta)[-1].split('.')[:-1]) != sample:
            sys.stderr.write(f'FASTA file name not matching sample name ({sample}, {fasta})')
            name.add(sample)

        if not os.path.exists(gff):
            sys.stderr.write(f'Could not find GFF file for {sample} ({gff})\n')
            missing.add(sample)
        if not os.path.exists(fasta):
            sys.stderr.write(f'Could not find FASTA file for {sample} ({fasta})\n')
            missing.add(sample)
        found.add(sample)

    if len(missing) > 0:
        sys.stderr.write(f'Could not locate {len(missing)} samples:\n')
        for sample in sorted(missing):
            sys.stderr.write(f'{sample}\n')
        sys.stderr.write('Exiting with an error code\n')
        sys.exit(1)

    f = open(os.path.join(options.out, 'unitigs_input.tsv'), 'w')
    f.write('ID\tPath\n')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{sample}\t{fasta}\n')
    f.close()

    f = open(os.path.join(options.out, 'input.tsv'), 'w')
    f.write('ID\tPath\n')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{sample}\t{fasta}\n')
    f.close()

    f = open(os.path.join(options.out, 'mash_input.txt'), 'w')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{fasta}\n')
    f.close()

    f = open(os.path.join(options.out, 'panaroo_input.txt'), 'w')
    for sample, row in m.iterrows():
        gff = row['gff']
        f.write(f'{gff}\n')
    f.close()

    f = open(os.path.join(options.out, 'annotate_input.txt'), 'w')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        gff = row['gff']
        f.write(f'{fasta}\t{gff}\tdraft\n')
    f.close()

    f = open(os.path.join(options.out, 'bcftools_input.txt'), 'w')
    for sample in m.index:
        path = os.path.join(options.out, f'snps/{sample}/snps.vcf.gz')
        f.write(f'{path}\n')
    f.close()

    for sample in sorted(found):
        print(sample)
