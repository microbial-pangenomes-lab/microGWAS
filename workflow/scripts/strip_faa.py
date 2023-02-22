#!/usr/bin/env python


import sys
import argparse
from Bio import SeqIO


def get_options():
    description = 'Strip FAA file if description lines (for SIFT4G)'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('faa',
                        help='Input protein fasta file')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    s = []
    for seq in SeqIO.parse(options.faa, 'fasta'):
        seq.description = seq.id
        s.append(seq)

    SeqIO.write(s, sys.stdout, 'fasta')
