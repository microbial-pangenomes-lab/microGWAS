#!/usr/bin/env Rscript

suppressPackageStartupMessages(library("argparse"))

parser <- ArgumentParser()
 
parser$add_argument("alignment",
                    help="Input alignment")
parser$add_argument("output",
                    help="Output table")

args <- parser$parse_args()

suppressPackageStartupMessages(library("siftr"))

sift_mat = predictFromAlignment(args$alignment, cores=1)
p = filterPredictions(sift_mat, score_thresh=1, ic_thresh=99)
write.table(p, file=args$output, sep="\t", row.names=F, quote=F)
