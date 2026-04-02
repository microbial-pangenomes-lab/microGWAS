#!/bin/bash

set -e -u -o pipefail -x

export CUDA_VISIBLE_DEVICES=1

# Check if running in CI mode (explicit command line flag)
CI_MODE=false
for arg in "$@"; do
    if [ "$arg" = "--ci" ]; then
        CI_MODE=true
        echo "Running in CI mode"
        break
    fi
done

# stop everything if we are risking to override
# a genuine GWAS run
# --- MODIFICA: Commentato per permettere di riprendere la run con cartella 'out' esistente ---
# if [ -d "../out" ]; then
#   echo "The output folder (../out) is present!";
#   echo "Please remove it and run this script again";
#   exit 1
# fi

# Define absolute paths for configuration and data files
CONFIG_BACKUP="$PWD/../config/config_backup.yaml"
CONFIG_TEMP="$PWD/../config/config.yaml"
DATA_BACKUP="$PWD/../data/data_backup.tsv"
DATA_TEMP="$PWD/../data/data.tsv"
SMALL_GENOMES="$PWD/"

# Define the cleanup function to restore state and remove temporary files
cleanup() {
    echo "Running cleanup..."
    
    # Restore configuration and data backups if they exist
    [ -f "$CONFIG_BACKUP" ] && mv "$CONFIG_BACKUP" "$CONFIG_TEMP"
    [ -f "$DATA_BACKUP" ] && mv "$DATA_BACKUP" "$DATA_TEMP"
    
    # Remove extracted directories
    rm -rf "${SMALL_GENOMES}small_fastas"
}

# Set trap to execute cleanup on script exit or interruption
trap cleanup EXIT SIGINT SIGTERM

# Backup data files
if [ -f "../data/data.tsv" ]; then
    cp ../data/data.tsv ../data/data_backup.tsv
fi

# Deploy the test phenotype file
cp test_data.tsv ../data/data.tsv

# Backup configuration file
if [ -f "../config/config.yaml" ]; then
    cp ../config/config.yaml ../config/config_backup.yaml
fi

# unpack the test dataset
tar -xvf small_fastas.tgz 

# skip lineages estimation
# these genomes are too small for it to work
cp lineages.txt ../data/
sed -i 's$lineages_file: \"out/lineages_mlst.txt\"$lineages_file: \"data/lineages.txt\"$g' ../config/config.yaml 

# download a smaller eggnog databse (gamma-proteobacteria)
sed -i 's$eggnogdb: \"2\"$eggnogdb: \"1236\"$g' ../config/config.yaml 

# ready to go
cd ..

# Also test the local assemblies functionality
# --- MODIFICA: Commentato per evitare di rifare il setup dei reference e il bootstrap ---
# zcat test/local_assemblies/536/genome.fasta.gz > test/local_assemblies/536/genome.fasta
# zcat test/local_assemblies/536/genome.gff.gz > test/local_assemblies/536/genome.gff
# zcat test/local_assemblies/536/genome.gbk.gz > test/local_assemblies/536/genome.gbk
# #
# if [ "$CI_MODE" = true ]; then
#     # In CI mode, only use local references
#     bash bootstrap.sh --local-dirs test/local_assemblies/536 Escherichia coli 536
#     sed -i 's$enrichment_reference: \"IAI39\"$enrichment_reference: "536"$g' config/config.yaml 
# else
#     # In normal mode, use both local and remote references
#     bash bootstrap.sh --local-dirs test/local_assemblies/536 Escherichia coli IAI39 GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1
# fi
#
# # reduce the size of the reference proteome
# # to speed up its annotation and rare variants analysis
# cp test/reference.faa data/

# first dry run
snakemake -np annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree --cores 18 --use-conda

if [ "$CI_MODE" = true ]; then
    echo "CI mode: skipping actual snakemake run"
else
    # actual run (brace yourself)
    snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree --cores 18 --use-conda
fi
