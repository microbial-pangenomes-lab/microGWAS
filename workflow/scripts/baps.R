#!/usr/bin/env Rscript

suppressPackageStartupMessages(library("argparse"))

parser <- ArgumentParser()
 
parser$add_argument("alignment",
                    help="MSA of isolates")
parser$add_argument("output",
                    help="BAPS clusters output")
parser$add_argument("--cores",
                    type="integer",
                    default=1, 
                    help="Number of cores to use [default %(default)s]")
parser$add_argument("--levels",
                    type="integer",
                    default=2, 
                    help="Number of levels [default %(default)s]")

args <- parser$parse_args()

suppressPackageStartupMessages(library("rhierbaps"))

# load MSA
snp.matrix <- load_fasta(args$alignment)

# run BAPS
hb.results <- hierBAPS(snp.matrix,
		       max.depth = args$levels,
		       n.cores = args$cores)

# save clusters
write.csv(hb.results$partition.df,
	  file = args$output, 
	  row.names = FALSE,
	  quote = FALSE)
