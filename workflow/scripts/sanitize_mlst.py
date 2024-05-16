#!/usr/bin/env python


import os
import argparse


def get_options():
    description = 'Remove paths and file extensions from mlst results'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('mlst',
                        help='Output of mlst (two columns, no header)')

    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()

    for l in open(options.mlst):
        fname, st = l.rstrip().split('\t')
        sample = os.path.split(fname)[1]
        sample = '.'.join(sample.split('.')[:-1])
        print(f'{sample}\t{st}')
