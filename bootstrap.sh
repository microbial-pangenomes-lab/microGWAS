#!/bin/bash

if [ $# -ne 4 ]; then
  echo "Error: the bootstrapping script requires exactly 4 positional arguments."
  echo "Usage: $0 GENUS SPECIES REFERENCE ASSEMBLIES"
  cat << EOF
Arguments:
  GENUS                Genus of the species under study (e.g. Escherichia)
  SPECIES              Species of the species under study (e.g. coli)
  REFERENCE            Strain name for the reference to be used for rare variants (e.g. IAI39, name should be the one NCBI uses)
  ASSEMBLIES           Comma separated list of NCBI assembly IDs to be downloaded as references (e.g. GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1)
EOF
  exit 1
fi

GENUS=$1
SPECIES=$2
REFERENCE=$3
ASSEMBLIES=$4

# this script requires ncbi-genome-download, biopython and gffutils

set -e -o pipefail -u

mkdir -p out
mkdir -p out/logs

echo -e "ID\tPath" > out/unitigs_input.tsv
echo -e "ID\tPath" > out/inputs.tsv
cat /dev/null > out/mash_input.txt
cat /dev/null > out/panaroo_input.txt
cat /dev/null > out/annotate_input.txt
for strain in $(tail -n+2 data/data.tsv | awk -F'\t' '{print $1}');
do
  fasta="data/fastas/"$strain".fasta";
  gff="data/gffs/"$strain".gff";
  if [ -f "$fasta" ] && [ -f "$gff" ];
  then
    echo $strain;
    echo "data/fastas/"$strain".fasta" >> out/mash_input.txt;
    echo "data/gffs/"$strain".gff" >> out/panaroo_input.txt;
    echo -e $strain"\tdata/fastas/"$strain".fasta" >> out/unitigs_input.tsv;
    echo -e $strain"\tdata/fastas/"$strain".fasta" >> out/inputs.tsv;
    echo -e "data/fastas/"$strain".fasta\tdata/gffs/"$strain".gff\tdraft" >> out/annotate_input.txt;
  fi;
done

ncbi-genome-download -H -F gff,fasta,genbank,protein-fasta -A $ASSEMBLIES -p 1 -o data/references bacteria
mkdir -p data/references/fastas
mkdir -p data/references/gffs
mkdir -p data/references/faas
mkdir -p data/references/gbks
for ref in $(ls data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/);
do
  echo $ref;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_genomic.fna.gz > data/references/fastas/$ref.fasta;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_genomic.gff.gz > /tmp/$ref.gff;
  python3 workflow/scripts/convert_refseq_to_prokka_gff.py -g /tmp/$ref.gff -f data/references/fastas/$ref.fasta -o data/references/gffs/$ref.gff;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_genomic.gbff.gz > data/references/gbks/$ref.gbk;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_protein.faa.gz > data/references/faas/$ref.faa;
  echo "data/references/fastas/"$ref".fasta" >> out/mash_input.txt;
  echo "data/references/gffs/"$ref".gff" >> out/panaroo_input.txt;
  echo -e $ref"\tdata/references/fastas/"$ref".fasta" >> out/unitigs_input.tsv;
  echo -e "data/references/fastas/"$ref".fasta\tdata/references/gffs/"$ref".gff\tref" >> out/annotate_input.txt;
done

python3 workflow/scripts/gbk2faa.py data/references/gbks/$REFERENCE.gbk > data/sift4g.faa
cp data/references/gffs/$REFERENCE.gff data/reference.gff
cp data/references/gbks/$REFERENCE.gbk data/reference.gbk

tail -n+2 out/unitigs_input.tsv > out/poppunk_input.txt
