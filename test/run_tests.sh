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
mkdir -p small_gffs
# generate the full GFF files
for i in $(ls small_fastas);
do
  cat stripped_small_gffs/$(basename $i .fasta).gff > small_gffs/$(basename $i .fasta).gff;
  echo "##FASTA" >> small_gffs/$(basename $i .fasta).gff;
  cat small_fastas/$i >> small_gffs/$(basename $i .fasta).gff;
done

# move phenotypic data
cp data.tsv ../data/

# skip lineages estimation
# these genomes are too small for it to work
cp lineages.txt ../data/
sed -i 's$lineages_file: \"out/lineages_mlst.txt\"$lineages_file: \"data/lineages.txt\"$g' ../config/config.yaml 

# download a smaller eggnog databse (gamma-proteobacteria)
sed -i 's$eggnogdb: \"2\"$eggnogdb: \"1236\"$g' ../config/config.yaml 

# ready to go
cd ..
# Also test the local assemblies functionality
zcat test/local_assemblies/536/genome.fasta.gz > test/local_assemblies/536/genome.fasta
zcat test/local_assemblies/536/genome.gff.gz > test/local_assemblies/536/genome.gff
zcat test/local_assemblies/536/genome.gbk.gz > test/local_assemblies/536/genome.gbk
#
bash bootstrap.sh --local-dirs test/local_assemblies/536 Escherichia coli IAI39 GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1
# reduce the size of the reference proteome
# to speed up its annotation and rare variants analysis
cp test/reference.faa data/
# first dry run
snakemake -np annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree --cores 8 --use-conda
# actual run (brace yourself)
snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree --cores 8 --use-conda
