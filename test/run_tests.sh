#!/bin/bash

set -e -u -o pipefail -x

# stop everything if we are risking to override
# a genuine GWAS run
if [ -d "../out" ]; then
  echo "The output folder (../out) is present!";
  echo "Please remove it and run this script again";
  exit 1
fi

# unpack the test dataset
tar -xvf small_fastas.tgz 
tar -xvf stripped_small_gffs.tgz 
mv small_fastas ../data/fastas
mv stripped_small_gffs ../data/gffs
# generate the full GFF files
for i in $(ls ../data/fastas);
do
  echo "##FASTA" >> ../data/gffs/$(basename $i .fasta).gff;
  cat ../data/fastas/$i >>../data/gffs/$(basename $i .fasta).gff;
done

# move phenotypic data
cp data.tsv ../data/

# skip lineages estimation
# these genomes are too small for it to work
cp lineages.txt ../data/
sed -i 's$lineages_file: \"out/lineages_mlst.txt\"$lineages_file: \"data/lineages.txt\"$g' ../config/config.yaml 

# ready to go
cd ..
bash bootstrap.sh Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1
# first dry run
snakemake -np annotate_summary panfeed map_back heritability enrichment qq_plots tree --cores 8 --use-conda --conda-frontend mamba
# actual run (brace yourself)
snakemake -p annotate_summary panfeed map_back heritability enrichment qq_plots tree --cores 8 --use-conda --conda-frontend mamba
