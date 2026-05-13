#!/usr/bin/env python

def get_options():
    import argparse

    # create the top-level parser
    description = "Check which samples are to be used in the GWAS pipeline"
    parser = argparse.ArgumentParser(description = description)

    parser.add_argument('data', action='store',
                        help='Data input file (first column is sample names, '
                             'a column named "fasta" should '
                             'be present, indicating the absolute or relative path '
                             'to the assemblies. It is assumed '
                             'that all file names are in the form SAMPLE.fasta). '
                             'An optional column named "gff" can also be provided, '
                             'with the same conventions, to skip the ggcaller step.')
    parser.add_argument('--out', action='store',
                        default='out',
                        help='Output directory in which to write the output files '
                             '(default: %(default)s)')
    parser.add_argument('--config', action='store',
                        default='config/config.yaml',
                        help='Path to the pipeline config file. The "use_user_gffs" '
                             'flag in this file is flipped to true/false depending '
                             'on whether the "gff" column is present in the input '
                             '(default: %(default)s)')

    return parser.parse_args()


def _flip_use_user_gffs(config_path, value):
    """Set `use_user_gffs: <value>` in the YAML config, in place.

    Operates as a line-based edit so the rest of the file (comments,
    ordering, formatting) is preserved. If the key is not present it is
    appended at the end of the file under a small comment header.
    """
    import os
    import re

    if not os.path.exists(config_path):
        return False

    with open(config_path) as fh:
        lines = fh.readlines()

    new_value = "true" if value else "false"
    pattern = re.compile(r'^(\s*)use_user_gffs(\s*):(\s*).*$')

    found = False
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if m:
            indent, pre_colon, post_colon = m.group(1), m.group(2), m.group(3) or ' '
            lines[i] = f"{indent}use_user_gffs{pre_colon}:{post_colon}{new_value}\n"
            found = True
            break

    if not found:
        if lines and not lines[-1].endswith('\n'):
            lines[-1] = lines[-1] + '\n'
        lines.append('\n')
        lines.append(f'use_user_gffs: {new_value}\n')

    with open(config_path, 'w') as fh:
        fh.writelines(lines)

    return True


if __name__ == "__main__":
    options = get_options()

    import os
    import sys
    import pandas as pd

    m = pd.read_csv(options.data, sep='\t', index_col=0)
    if 'fasta' not in m.columns:
        sys.stderr.write('Input data file must contain a "fasta" column\n')
        sys.exit(1)

    has_gff_column = 'gff' in m.columns

    found = set()
    missing = set()
    name = set()
    missing_gff = set()
    name_gff = set()
    for sample, row in m.iterrows():
        fasta = row['fasta']

        # check that the file names follow the SAMPLE.EXT convention
        if '.'.join(os.path.split(fasta)[-1].split('.')[:-1]) != str(sample):
            sys.stderr.write(f'FASTA file name not matching sample name ({sample}, {fasta})')
            name.add(sample)

        # Check only for FASTA existence
        if not os.path.exists(fasta):
            sys.stderr.write(f'Could not find FASTA file for {sample} ({fasta})\n')
            missing.add(sample)

        # Same checks on the GFF column when present
        if has_gff_column:
            gff = row['gff']
            if pd.isna(gff) or str(gff).strip() == '':
                sys.stderr.write(f'Empty "gff" entry for sample {sample}\n')
                missing_gff.add(sample)
            else:
                gff = str(gff)
                if '.'.join(os.path.split(gff)[-1].split('.')[:-1]) != str(sample):
                    sys.stderr.write(f'GFF file name not matching sample name ({sample}, {gff})\n')
                    name_gff.add(sample)
                if not os.path.exists(gff):
                    sys.stderr.write(f'Could not find GFF file for {sample} ({gff})\n')
                    missing_gff.add(sample)

        found.add(sample)

    if len(missing) > 0:
        sys.stderr.write(f'Could not locate {len(missing)} samples (FASTA):\n')
        for sample in sorted(missing):
            sys.stderr.write(f'{sample}\n')
        sys.stderr.write('Exiting with an error code\n')
        sys.exit(1)

    if has_gff_column and len(missing_gff) > 0:
        sys.stderr.write(f'Could not locate {len(missing_gff)} GFF files:\n')
        for sample in sorted(missing_gff):
            sys.stderr.write(f'{sample}\n')
        sys.stderr.write('Exiting with an error code\n')
        sys.exit(1)

    f = open(os.path.join(options.out, 'unitigs_input.tsv'), 'w')
    f.write('ID\tPath\n')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{sample}\t{fasta}\n')
    f.close()

    f = open(os.path.join(options.out, 'input.tsv'), 'w')
    f.write('ID\tPath\n')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{sample}\t{fasta}\n')
    f.close()

    f = open(os.path.join(options.out, 'mash_input.txt'), 'w')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{fasta}\n')
    f.close()

    f = open(os.path.join(options.out, 'ggcaller_input.txt'), 'w')
    for sample, row in m.iterrows():
        fasta = row['fasta']
        f.write(f'{fasta}\n')
    f.close()
    
    f = open(os.path.join(options.out, 'panaroo_input.txt'), 'w')
    for sample, row in m.iterrows():
        if has_gff_column:
            gff = row['gff']
        else:
            gff = f'out/ggcaller/GFF/{sample}.gff'
        f.write(f'{gff}\n')
    f.close()

    f = open(os.path.join(options.out, 'ggcaller_gffs.txt'), 'w')
    for sample, row in m.iterrows():
        if has_gff_column:
            gff = row['gff']
        else:
            gff = f'out/ggcaller/GFF/{sample}.gff'
        f.write(f'{gff}\n')
    f.close()

    if has_gff_column:
        f = open(os.path.join(options.out, 'user_gffs.tsv'), 'w')
        f.write('sample\tgff\n')
        for sample, row in m.iterrows():
            f.write(f"{sample}\t{row['gff']}\n")
        f.close()

        # different annotate_input: point to the user-provided GFFs directly
        f = open(os.path.join(options.out, 'annotate_input.txt'), 'w')
        for sample, row in m.iterrows():
            fasta = row['fasta']
            gff = row['gff']
            f.write(f'{fasta}\t{gff}\tdraft\n')
        f.close()
    else:
        f = open(os.path.join(options.out, 'annotate_input.txt'), 'w')
        for sample, row in m.iterrows():
            fasta = row['fasta']
            # Point blindly to the future generated GFF from ggCaller
            f.write(f'{fasta}\tout/ggcaller/GFF/{sample}.gff\tdraft\n')
        f.close()

    f = open(os.path.join(options.out, 'bcftools_input.txt'), 'w')
    for sample in m.index:
        path = os.path.join(options.out, f'snps/{sample}/snps.vcf.gz')
        f.write(f'{path}\n')
    f.close()

    # Flip the `use_user_gffs` flag in the pipeline config
    if _flip_use_user_gffs(options.config, has_gff_column):
        if has_gff_column:
            sys.stderr.write(
                f'\nFound a "gff" column in {options.data}: '
                f'{len(found)} user-provided GFF files validated.\n'
                f'Set `use_user_gffs: true` in {options.config} '
                f'(ggcaller will be skipped).\n'
            )
        else:
            sys.stderr.write(
                f'\nNo "gff" column in {options.data}: '
                f'set `use_user_gffs: false` in {options.config} '
                f'(ggcaller will be run as usual).\n'
            )
    else:
        sys.stderr.write(
            f'\nWarning: config file {options.config} not found; '
            f'`use_user_gffs` flag was not updated.\n'
        )

    for sample in sorted(found):
        print(sample)
