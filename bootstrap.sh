#!/bin/bash

LOCAL_DIRS_ARG=""
ASSEMBLIES=""
GENUS=""
SPECIES=""
REFERENCE=""


# --- Argument Parsing with getopt ---
# Note: Using getopt (the util) not the Bash builtin for long options
# l: requires an argument
TEMP=$(getopt -o l: --long local-dirs: -n "$0" -- "$@")

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

while true; do
  case "$1" in
    -l | --local-dirs ) LOCAL_DIRS_ARG="$2"; shift 2 ;;
    -- ) shift; break ;;
    * ) break ;; # Should not happen with getopt definition unless error
  esac
done

# We now require at least 3 positional arguments, and optionally a 4th (ASSEMBLIES)
if [ "$#" -lt 3 ]; then
  echo "Error: At least 3 positional arguments are required."
  echo "Usage: $0 [--local-dirs DIR1,...] GENUS SPECIES REFERENCE [ASSEMBLIES]"
      cat << EOF

Arguments:
  GENUS                Genus of the species under study (e.g. Escherichia)
  SPECIES              Species of the species under study (e.g. coli)
  REFERENCE            Strain name for the reference genome (e.g. IAI39). Must match either a local dir basename or an NCBI assembly ID name.
  ASSEMBLIES           (Optional if --local-dirs used) Comma separated list of NCBI assembly IDs (e.g. GCF_000013305.1,...)

Optional Arguments:
  --local-dirs DIR,... Comma separated list of directories containing pre-downloaded genomes.
                       Each directory must contain:
                         - genome.fasta (genomic FASTA)
                         - genome.gff (GFF3 annotation)
                         - genome.gbk (GenBank format)
                         - genome.faa (protein FASTA, optional, will be generated from GBK if missing)
                       The basename of the directory will be used as the strain identifier.
EOF
  exit 1
fi

GENUS=$1
SPECIES=$2
REFERENCE=$3
# Assign ASSEMBLIES only if the 4th argument exists
if [ "$#" -ge 4 ]; then
    ASSEMBLIES=$4
fi

if [ -z "$LOCAL_DIRS_ARG" ] && [ -z "$ASSEMBLIES" ]; then
    echo "Error: You must provide either --local-dirs or the ASSEMBLIES argument (or both)."
    exit 1
fi

# this script requires ncbi-genome-download, biopython and gffutils

set -e -o pipefail

mkdir -p out
mkdir -p out/logs
mkdir -p data/references/fastas
mkdir -p data/references/gffs
mkdir -p data/references/faas
mkdir -p data/references/gbks

> out/mash_input.txt
> out/panaroo_input.txt
> out/unitigs_input.tsv
> out/annotate_input.txt
> out/poppunk_input.txt

python workflow/scripts/aid_bootstrap.py data/data.tsv --out out

# Handle reference genomes (RefSeq or locally, or both)

if [ -n "$LOCAL_DIRS_ARG" ]; then
  echo "Processing local assemblies..."
  IFS=',' read -ra LOCAL_DIRS <<< "$LOCAL_DIRS_ARG"
  for local_dir in "${LOCAL_DIRS[@]}"; do
    if [ ! -d "$local_dir" ]; then
        echo "Error: Local assembly directory not found: $local_dir"
        exit 1
    fi
    ref=$(basename "$local_dir")
    echo "Processing local reference: $ref from $local_dir"

    # Define expected input files
    local_fasta="$local_dir/genome.fasta"
    local_gff="$local_dir/genome.gff"
    local_gbk="$local_dir/genome.gbk"
    local_faa="$local_dir/genome.faa" # Optional

    # Check required files exist
    missing_files=0
    for f in "$local_fasta" "$local_gff" "$local_gbk"; do
        if [ ! -f "$f" ]; then
            echo "Error: Missing required file '$f' in local directory $local_dir"
            missing_files=1
        fi
    done
    if [ $missing_files -eq 1 ]; then
        exit 1
    fi

    mkdir -p "data/references/human_readable/refseq/"
    mkdir -p "data/references/human_readable/refseq/bacteria/"
    mkdir -p "data/references/human_readable/refseq/bacteria/$GENUS/"
    mkdir -p "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/"
    mkdir -p "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/"

    # Copy/Link files to structured directories
    gzip "$local_fasta" -c > "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/${ref}_genomic.fna.gz"
    gzip "$local_gff" -c > "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/${ref}_genomic.gff.gz"
    gzip "$local_gbk" -c > "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/${ref}_genomic.gbff.gz"
    
    # Handle protein FASTA
    if [ -f "$local_faa" ]; then
       gzip "$local_faa" -c > "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/${ref}_protein.faa.gz"
       echo "  Using provided protein FASTA."
    else
       echo "  Generating protein FASTA from GenBank..."
       python3 workflow/scripts/gbk2faa.py "$local_gbk" > "$local_faa"
       gzip "$local_faa" -c > "data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/${ref}_protein.faa.gz"
    fi

  done
fi

if [ -n "$ASSEMBLIES" ]; then
    echo "Processing remote assemblies from NCBI's RefSeq..."
    ncbi-genome-download -H -F gff,fasta,genbank,protein-fasta -A $ASSEMBLIES -p 1 -o data/references bacteria
fi

for ref in $(ls data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/);
do
  echo $ref;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_genomic.fna.gz > data/references/fastas/$ref.fasta;
  tempfile=$(mktemp);
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_genomic.gff.gz > $tempfile;
  python3 workflow/scripts/convert_refseq_to_prokka_gff.py -g $tempfile -f data/references/fastas/$ref.fasta -o data/references/gffs/$ref.gff;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_genomic.gbff.gz > data/references/gbks/$ref.gbk;
  zcat data/references/human_readable/refseq/bacteria/$GENUS/$SPECIES/$ref/*_protein.faa.gz > data/references/faas/$ref.faa;
  echo "data/references/fastas/"$ref".fasta" >> out/mash_input.txt;
  echo "data/references/gffs/"$ref".gff" >> out/panaroo_input.txt;
  echo -e $ref"\tdata/references/fastas/"$ref".fasta" >> out/unitigs_input.tsv;
  echo -e "data/references/fastas/"$ref".fasta\tdata/references/gffs/"$ref".gff\tref" >> out/annotate_input.txt;
done

python3 workflow/scripts/gbk2faa.py data/references/gbks/$REFERENCE.gbk > data/reference.faa
cp data/references/gffs/$REFERENCE.gff data/reference.gff
cp data/references/gbks/$REFERENCE.gbk data/reference.gbk

tail -n+2 out/unitigs_input.tsv > out/poppunk_input.txt
