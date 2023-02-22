#!/bin/bash

# this script requires blast, ncbi-genome-download, biopython and gffutils

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

ncbi-genome-download -H -F gff,fasta,genbank,protein-fasta -A GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 -p 1 -o data/references bacteria
mkdir -p data/references/fastas
mkdir -p data/references/gffs
mkdir -p data/references/faas
mkdir -p data/references/gbks
for ref in $(ls data/references/human_readable/refseq/bacteria/Escherichia/coli/);
do
  echo $ref;
  zcat data/references/human_readable/refseq/bacteria/Escherichia/coli/$ref/*_genomic.fna.gz > data/references/fastas/$ref.fasta;
  zcat data/references/human_readable/refseq/bacteria/Escherichia/coli/$ref/*_genomic.gff.gz > /tmp/$ref.gff;
  python3 workflow/scripts/convert_refseq_to_prokka_gff.py -g /tmp/$ref.gff -f data/references/fastas/$ref.fasta -o data/references/gffs/$ref.gff;
  zcat data/references/human_readable/refseq/bacteria/Escherichia/coli/$ref/*_genomic.gbff.gz > data/references/gbks/$ref.gbk;
  zcat data/references/human_readable/refseq/bacteria/Escherichia/coli/$ref/*_protein.faa.gz > data/references/faas/$ref.faa;
  echo "data/references/fastas/"$ref".fasta" >> out/mash_input.txt;
  echo "data/references/gffs/"$ref".gff" >> out/panaroo_input.txt;
  echo -e $ref"\tdata/references/fastas/"$ref".fasta" >> out/unitigs_input.tsv;
  echo -e "data/references/fastas/"$ref".fasta\tdata/references/gffs/"$ref".gff\tref" >> out/annotate_input.txt;
done

python3 workflow/scripts/gbk2faa.py data/references/gbks/IAI39.gbk > data/sift4g.faa

tail -n+2 out/unitigs_input.tsv > out/poppunk_input.txt
