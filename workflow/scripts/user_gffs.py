#!/usr/bin/env python3
"""Build the GFF list from user-provided GFF files.

Reads the sample list from `fasta_list` (typically `mash_input`),
matches each sample to a `<sample>.gff` or `<sample>.gff3` file in
`user_dir`, and writes the absolute paths of the matching GFFs (in the
same order as the samples) to `out_gffs`.

Two empty placeholder files are also created (`out_calls`, `out_gfa`)
to mirror the outputs declared by the `ggcaller` rule, so that the
DAG stays consistent. They are not consumed by any downstream rule.

Fails with a non-zero exit code (and a clear error message) if no GFF
files are found, or if any sample is missing its GFF.
"""

import argparse
import glob
import os
import sys


def collect_user_gffs(user_dir):
    """Return a sorted list of .gff and .gff3 files in `user_dir`."""
    return sorted(
        glob.glob(os.path.join(user_dir, "*.gff")) +
        glob.glob(os.path.join(user_dir, "*.gff3"))
    )


def read_sample_names(fasta_list):
    """Read sample names from a fasta_list file (one path per line).

    The sample name is the basename of the path without its extension.
    """
    samples = []
    with open(fasta_list) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            samples.append(os.path.splitext(os.path.basename(line))[0])
    return samples


def build_gff_index(gff_paths):
    """Map sample name -> absolute path of its GFF."""
    return {
        os.path.splitext(os.path.basename(g))[0]: os.path.abspath(g)
        for g in gff_paths
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fasta-list", required=True,
                        help="Path to the mash_input file (one fasta path per line).")
    parser.add_argument("--user-dir", required=True,
                        help="Directory containing user-provided GFF files.")
    parser.add_argument("--out-gffs", required=True,
                        help="Output: file with the list of GFF paths.")
    parser.add_argument("--out-calls", required=True,
                        help="Output: empty placeholder mirroring ggcaller_calls.")
    parser.add_argument("--out-gfa", required=True,
                        help="Output: empty placeholder mirroring ggcaller_gfa.")
    parser.add_argument("--ggcaller-dir", required=True,
                        help="Directory mirroring ggcaller_dir (created if missing).")
    args = parser.parse_args()

    os.makedirs(args.ggcaller_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.out_gffs) or ".", exist_ok=True)

    gffs = collect_user_gffs(args.user_dir)
    if not gffs:
        sys.exit(
            f"ERROR: no GFF files found in {args.user_dir!r}. "
            f"Provide files named <sample>.gff (or .gff3), "
            f"or unset `user_gffs_dir` in the config."
        )

    samples = read_sample_names(args.fasta_list)
    available = build_gff_index(gffs)
    missing = [s for s in samples if s not in available]

    print(f"Found {len(gffs)} user-provided GFF files in {args.user_dir}",
          file=sys.stderr)
    print(f"Samples in {args.fasta_list}: {len(samples)}", file=sys.stderr)

    if missing:
        preview = missing[:10]
        more = " ..." if len(missing) > 10 else ""
        sys.exit(
            f"ERROR: missing user-provided GFF files for {len(missing)} "
            f"sample(s): {preview}{more}. Each sample must have a file "
            f"named <sample>.gff (or .gff3) in {args.user_dir!r}."
        )

    with open(args.out_gffs, "w") as fh:
        for s in samples:
            fh.write(available[s] + "\n")

    # placeholders to keep the DAG symmetric with the ggcaller rule
    open(args.out_calls, "a").close()
    open(args.out_gfa, "a").close()

    print(f"Wrote {len(samples)} GFF paths to {args.out_gffs}", file=sys.stderr)


if __name__ == "__main__":
    main()
