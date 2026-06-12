#!/usr/bin/env python


def get_options():
    import argparse

    description = ('Extract a subtable from the pangenome-wide eggnog-mapper '
                  'annotations, keeping only the orthologous groups (OGs) of '
                  'interest. This avoids re-running emapper.py for every '
                  'association summary.')
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('annotations',
                        help='Pangenome-wide eggnog-mapper output '
                             '(i.e. pangenome.emapper.annotations)')

    parser.add_argument('--groups',
                        default=None,
                        help='OGs to keep (tab-delimited summary file, OGs as '
                             'the first column) [Default: all of them]')
    parser.add_argument('--struct',
                        default=False,
                        action='store_true',
                        help='Tab-delimited summary file is a structural '
                             'variant file (OGs joined by "-")')

    parser.add_argument('--pangenome',
                        default=None,
                        help='Panaroo\'s output (gene_presence_absence.csv), '
                             'required when filtering by --focus-strain')
    parser.add_argument('--focus-strain',
                        default=None,
                        action='append',
                        help='Keep only OGs found in this strain '
                             '(can be passed multiple times)')
    parser.add_argument('--only-focus',
                        default=False,
                        action='store_true',
                        help='Only keep OGs that are present in the focus '
                             'strain(s) [requires --focus-strain]')

    return parser.parse_args()


def ogs_from_groups(path, struct):
    import sys
    import pandas as pd

    try:
        ogs = pd.read_csv(path, sep='\t', index_col=0).index
    except Exception as e:
        sys.stderr.write(f'Could not parse OGs ("{str(e)}")\n')
        return set()
    if struct:
        return {y for x in set(ogs) for y in str(x).split('-')}
    return set(str(x) for x in ogs)


def ogs_from_focus(pangenome, focus_strains):
    import sys
    import pandas as pd

    roary = pd.read_csv(pangenome,
                        sep=',',
                        low_memory=False,
                        index_col=0)
    # drop the two extra info columns panaroo adds after the OG name
    roary.drop(list(roary.columns[:2]), axis=1, inplace=True)

    missing = [s for s in focus_strains if s not in roary.columns]
    if missing:
        sys.stderr.write('Focus strain(s) not found in the pangenome: '
                         f'{", ".join(missing)}\n')
    present = [s for s in focus_strains if s in roary.columns]
    if not present:
        return set()
    sub = roary[present]
    return set(str(og) for og in sub.index[sub.notna().any(axis=1)])


if __name__ == "__main__":
    options = get_options()

    import sys

    ogs = None
    if options.groups is not None:
        ogs = ogs_from_groups(options.groups, options.struct)
    elif options.only_focus or options.focus_strain is not None:
        if options.pangenome is None or options.focus_strain is None:
            sys.stderr.write('--only-focus/--focus-strain require both '
                             '--pangenome and --focus-strain\n')
            sys.exit(1)
        ogs = ogs_from_focus(options.pangenome, options.focus_strain)

    if ogs is not None and len(ogs) == 0:
        sys.stderr.write('No OGs found\n')
        sys.exit(0)

    # Stream the annotations file: comment lines (the 4-line header and the
    # 3-line footer that eggnog-mapper writes, plus the "#query" column header)
    # are preserved verbatim so that enhance_summary.py keeps working unchanged;
    # data rows are kept only when their OG (first column) is in the set.
    with open(options.annotations) as handle:
        for line in handle:
            if line.startswith('#'):
                sys.stdout.write(line)
                continue
            if ogs is None:
                sys.stdout.write(line)
                continue
            og = line.split('\t', 1)[0]
            if og in ogs:
                sys.stdout.write(line)
