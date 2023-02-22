#!/usr/bin/env python


import os
import sys


def get_options():
    import argparse

    description = 'Map filtered kmers to original genomes'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('kmers',
                        help='Filtered kmers table')
    parser.add_argument('genome',
                        help='Original genome fasta file directory '
                             '(format SAMPLE.fasta)')

    parser.add_argument("--bwa",
                        help="Location of bwa executable "
                        "[default=bwa]",
                        default="bwa")
    parser.add_argument("--bwa-algorithm",
                        help="bwa algorithm "
                        "[default=fastmap]",
                        default="fastmap")
    parser.add_argument("--tmp-prefix",
                        help="Directory to store temporary files "
                        "[default=./]",
                        default=os.getcwd())
    parser.add_argument('--gff',
                        default=None,
                        help='Annotation directory in GFF format '
                             '(format SAMPLE.gff)')
    parser.add_argument("--pangenome",
                        help="Panaroo's genes presence/absence table (w/ gene names)",
                        default=None)
    parser.add_argument("--print-details",
                        help="Print mapping positions",
                        default=False,
                        action='store_true')

    return parser.parse_args()


def extract_genes(bedtools_intervals, rd=None):
    if rd is None:
        rd = {}
    annotations = {}
    for match in bedtools_intervals.features():
        kmer_id, hit_id = match.fields[3].split("_")
        annotations[kmer_id] = {}

        ID = None
        gene = None
        for tag in match.fields[15].split(";"):
            parse_tag = re.search('^(.+)=(.+)$', tag)
            if parse_tag:
                if parse_tag.group(1) == "ID" and ID is None:
                    ID = parse_tag.group(2)
        if gene is None:
            if ID is not None:
                gene = ID
            else:
                gene = ""

        annotations[kmer_id][int(hit_id)] = rd.get(gene, gene)

    return annotations


if __name__ == "__main__":
    options = get_options()

    import os
    import shutil
    if options.gff is not None:
        import re
        import tempfile
        import subprocess
        import pybedtools
        pybedtools.helpers.set_tempdir(options.tmp_prefix)
    import pandas as pd
    from Bio import SeqIO

    from bwa import bwa_index
    from bwa import bwa_iter

    kmers_file = open(options.kmers)
    _ = kmers_file.readline()
    kmers = sorted([kmer.rstrip().split()[0] for kmer in kmers_file])
    if len(kmers) == 0:
        sys.exit(0)
    kmers_file.close()

    # read pangenome table once
    if options.pangenome is not None:
        roary = pd.read_table(options.pangenome,
                              sep=',',
                              low_memory=False)
        roary.set_index('Gene', inplace=True)
        # Drop the other info columns
        roary.drop(list(roary.columns[:2]), axis=1, inplace=True)
        roary.reset_index(inplace=True)

    kmers_fasta = os.path.join(options.tmp_prefix, 'kmers.fasta')
    kmers_file = open(kmers_fasta, 'w')
    for idx, kmer in enumerate(kmers):
        kmers_file.write('>%d\n' % idx)
        kmers_file.write('%s\n' % kmer)
    kmers_file.close()

    # assumption: strain names are in the fasta file name
    for fgenome in os.listdir(options.genome):
        if not fgenome.endswith('.fasta'):
            continue
        strain_id = '.'.join(fgenome.split('.')[:-1])
        genome = strain_id

        # pangenome dictionary
        rd = {}
        if options.pangenome is not None:
            for strain in roary.columns[1:]:
                if strain != strain_id:
                    continue
                for x, y, in roary.set_index(strain)['Gene'].dropna().to_dict().items():
                    if str(x) == 'nan':
                        continue
                    # be aware of paralogs
                    for g in x.split(';'):
                        rd[g] = y


        if options.gff is not None:
            fgff = os.path.join(options.gff, f'{genome}.gff')
            # Fix ref annotation
            tmp_bed = tempfile.NamedTemporaryFile(dir=options.tmp_prefix)
            try:
                subprocess.run("gff2bed < " + fgff + " > " + tmp_bed.name, shell=True, check=True)
            except AttributeError:
                # python prior to 3.5
                subprocess.check_call("gff2bed < " + fgff + " > " + tmp_bed.name, shell=True)
            ref_annotation = pybedtools.BedTool(tmp_bed.name)
            filtered_ref = ref_annotation.filter(lambda x: True if x[7] == "CDS" else False).saveas(os.path.join(options.tmp_prefix, 'tmp_bed'))
            ref_annotation = pybedtools.BedTool(os.path.join(options.tmp_prefix, 'tmp_bed'))
            query_bed = tempfile.NamedTemporaryFile('w', dir=options.tmp_prefix)
            kmers = []
            map_pos = {}

        shutil.copy(os.path.join(options.genome, fgenome), options.tmp_prefix)
        genome_file = os.path.join(options.tmp_prefix, fgenome)
        bwa_index(genome_file)
        for mapping, kmer in zip(bwa_iter(genome_file, kmers_fasta, options.bwa_algorithm),
                                 SeqIO.parse(kmers_fasta, 'fasta')):
            if mapping.mapped:
                if not options.print_details:
                    print('\t'.join((genome, str(kmer.seq), 'mapped')))
                else:
                    if options.gff is None:
                        for pos in mapping.positions:
                            print('\t'.join((genome, str(kmer.seq))) + '\t' +
                                  '\t'.join([str(x) for x in pos]))
                    else:
                        map_pos[kmer.id] = []
                        for hit_idx, (contig, start, end, strand) in enumerate(mapping.positions):
                            query_bed.write('\t'.join([contig,
                                                       str(start), str(end),
                                                       kmer.id + "_" + str(hit_idx),
                                                       '0', strand]) + "\n")
                            map_pos[kmer.id].append((contig, start, end, strand))
                            kmers.append(kmer)

        if options.gff is not None:
            query_bed.flush()
            query_interval = pybedtools.BedTool(query_bed.name)
            sorted_query = query_interval.sort()

            in_genes = extract_genes(query_interval.intersect(b=ref_annotation,
                                                              s=False, stream=True,
                                                              wb=True), rd)
            up_genes = extract_genes(sorted_query.closest(b=ref_annotation,
                                                          s=False, D="ref", iu=True,
                                                          stream=True), rd)
            down_genes = extract_genes(sorted_query.closest(b=ref_annotation,
                                                            s=False, D="ref", id=True,
                                                            stream=True), rd)
            pybedtools.cleanup() # delete the bed file

            for kmer  in kmers:
                down = ''
                gene = ''
                up = ''
                for hit_idx, hit in enumerate(map_pos[kmer.id]):
                    if kmer.id in down_genes and hit_idx in down_genes[kmer.id]:
                        down = down_genes[kmer.id][hit_idx]
                    if kmer.id in in_genes and hit_idx in in_genes[kmer.id]:
                        gene = in_genes[kmer.id][hit_idx]
                    if kmer.id in up_genes and hit_idx in up_genes[kmer.id]:
                        up = up_genes[kmer.id][hit_idx]
                    print('\t'.join((genome, str(kmer.seq))) + '\t' +
                          '\t'.join([str(x) for x in hit]) + '\t' +
                          '\t'.join([down, gene, up]))


        # cleanup
        os.remove(genome_file)
        os.remove(genome_file + '.amb')
        os.remove(genome_file + '.ann')
        os.remove(genome_file + '.bwt')
        os.remove(genome_file + '.pac')
        os.remove(genome_file + '.sa')
