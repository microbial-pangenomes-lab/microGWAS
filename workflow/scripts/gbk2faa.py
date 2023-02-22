#!/usr/bin/env python

def get_options():
    import argparse

    # create the top-level parser
    description = "Convert a GenBank file to a protein fasta"
    parser = argparse.ArgumentParser(description = description)

    parser.add_argument('gbk', action='store',
                        help='GenBank file')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    from Bio import SeqIO

    for s in SeqIO.parse(options.gbk, 'genbank'):
        for f in s.features:
            if f.type != 'CDS':
                continue
            locus = f.qualifiers['locus_tag'][0]
            seq = f.qualifiers.get('translation', [None])[0]
            if seq is None:
                continue
            print(f'>{locus}\n{seq}')
