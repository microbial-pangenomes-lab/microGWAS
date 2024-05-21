#!/usr/bin/env python3
"""
Generate model predictions from Sequence UNET like models from Fasta or ProteinNet data.
"""
import os
import argparse
import sys
import pandas as pd
from Bio import SeqIO

import tensorflow as tf

from sequence_unet.models import load_trained_model
from sequence_unet.predict import predict_proteinnet, predict_sequence
from proteinnetpy.data import ProteinNetDataset, make_id_filter

def main():
    """
    Main function
    """
    args = parse_args()

    tf.config.threading.set_intra_op_parallelism_threads(args.cores)
    tf.config.threading.set_inter_op_parallelism_threads(args.cores)

    model = load_trained_model(args.model, args.model_dir, download=args.download)

    if args.proteinnet:
        data = ProteinNetDataset(path=args.proteinnet, preload=False)
        preds = predict_proteinnet(model, data, layers=args.layers,
								   contact=args.contacts, wide=args.wide,
                                   make_pssm=args.pssm)

    elif args.fasta:
        fasta = SeqIO.parse(args.fasta, format="fasta")
        preds = predict_sequence(model, sequences=fasta, layers=args.layers, 
                                 wide=args.wide, make_pssm=args.pssm)

    else:
        raise ValueError("One of --fasta or --proteinnet must be passed")

    for i, df in enumerate(preds):
        prot = str(df['gene'].values[0])
        sys.stderr.write(f'{i} {prot}\n')
        df.to_csv(os.path.join(args.output, f'{prot}.tsv.gz'),
                  sep="\t", index=False, header=True)

def arg_parser():
    """Argument parser"""
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('model', metavar="M", help="Model to predict with")

    inputs = parser.add_argument_group("Input Data")
    inputs.add_argument('--proteinnet', "-p", help="ProteinNet file")
    inputs.add_argument('--fasta', "-f", help="Fasta file")

    options = parser.add_argument_group("Options")
    options.add_argument('--contacts', "-c", help="Use contact graph input (required for pregraph models)", action="store_true")
    options.add_argument('--layers', "-l", help="Number of layers in bottom UNET modeli (all pretrained models have 6 layers)",
                         type=int, default=6)

    options.add_argument('--wide', "-w", help="Output a wide table", action="store_true")
    options.add_argument('--pssm', "-s", help="Convert output frequency predictions to PSSMs",
	                     action="store_true")

    options.add_argument('--model_dir', "-m", help="Directory to locate/download model files to")
    options.add_argument('--download', "-d", action="store_true",
                         help="Download model if not located")

    options.add_argument('--cores', type=int, default=8,
            help="Maximum number of CPU cores (default: %(default)d)")

    options.add_argument('--output', default='.',
            help="Output directory to store outputs (default: %(default)s)")

    return parser

def parse_args():
    """Process arguments"""
    parser = arg_parser()
    args = parser.parse_args()

    if args.fasta is None and args.proteinnet is None:
        raise ValueError("Use one of --proteinnet/-p or --fasta/-f")

    if args.fasta is not None and args.proteinnet is not None:
        raise ValueError("Use either --proteinnet/-p or --fasta/-f, not both")

    if args.fasta is not None and args.contacts:
        raise ValueError("Cannot use --contacts with Fasta input")

    return args

if __name__ == "__main__":
    main()
