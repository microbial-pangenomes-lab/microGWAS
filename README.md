# Snakemake workflow: Bacterial GWAS

A battery included snakemake pipeline to run bacterial GWAS on a set of assembled genomes.
Multiple phenotypes can be defined and used for the associations.

For each phenotype, the pipeline will run associations using 5 sets of genetic variants:

* individual unitigs
* gene presence/absence
* rare variants (i.e. gene burden test)
* gene cluster specific k-mers
* all unitigs combined (i.e. whole genome machine learning model)

For each set of genetic variants a number of downstream analyses will be run to provide
annotated results and functional enrichments.

It will additionally compute the heritability of each phenotype using
the lineage information and the whole set of unitigs.

It can also optionally compute a phylogenetic tree of all samples.

## Quick start

Make a copy of this repository (optionally you can first create a new repository by clicking on the "Use this template" button
from Github's interface), including the submodules:

    git clone --recursive https://github.com/microbial-pangenomes-lab/gwas_template.git MyGWAS
    cd MyGWAS

Save your phenotype table as a tab-separated file as `data/data.tsv`.
The first column should contain the sample names, then there should be two columns
listing the relative or absolute path to the assemblies (`fasta`, SAMPLE.fasta) and annotations (`gff`, SAMPLE.gff),
and subsequent columns should
contain the target phenotype(s). Additional columns are allowed and will be simply ignored.
An example file can be found in the `test` directory (`test/data.tsv`).

Edit the `params` section of the `config/config.yaml` file (at the top), and indicate the name
of the phenotypes to be used in the association(s) (i.e. edit the `targets` variable).
Also change the mlst scheme to be used to compute lineages and the name of the references to be used
for annotation of hits. For convenience the defaults for E. coli are placed as defaults, and those
for P. aeruginosa are commented.

Create a symbolic link to the directory in which the databases for eggnog-mapper have been placed:

    ln -s /fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/ data/eggnog-mapper

Note: the above path would likely be different in your system. The best way to get these files is to install
`eggnog-mapper` using a `conda` environment and then use the `download_eggnog_data.py` command.

Create and activate a `conda` environment to run the bootstrapping script and the pipeline (named `microGWAS`, can be skipped if it's already present):

    conda env create -f environment.yml
    conda activate microGWAS

Then run the bootstrapping script to populate the input files for the pipeline and download the reference genomes
used for annotation of hits and the rare variants analyses. The following example works for E. coli (and downloads the references listed by default in `config/config.yaml`):

    bash bootstrap.sh Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 

And the following works for P. aeruginosa (and matches the references commented in `config/config.yaml`):

    bash bootstrap.sh Pseudomonas aeruginosa UCBPP-PA14 GCF_000006765.1,GCF_000014625.1 

You are now ready to run the full pipeline! The following example runs all the analyses using 24 cores and `mamba` as the conda backend
to install each environment:

    snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree --cores 24 --verbose --use-conda --conda-frontend mamba
    
The following example instead uses "vanilla" `conda` and skips the generation of the phylogenetic tree:

    snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots --cores 24 --verbose --use-conda

## Outputs

| Output file                         |  Description                                                                                                                                                                                                               |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| annotated_gpa_summary.tsv           |                                                                                                                                                                                                                                |
| annotated_rare_summary.tsv          |                                                                                                                                                                                                                                |
| annotated_summary.tsv               |                                                                                                                                                                                                                                |
| COG.tsv, COG_gpa.tsv, COG_rare.tsv  | GO functional enrichment for test unitigs, gene presence/absence and rare variants. Columns of interests are the COG category, and the qvalue<br>or empirical-qvalue as they are adjusted for multiple test corrections.       |
| GO.tsv, GO_gpa.tsv,GO_rare.tsv      | GO functional enrichment for test unitigs, gene presence/absence and rare variants. Columns of interests are the COG category, and the qvalue<br>or empirical-qvalue as they are adjusted for multiple test corrections.       |
| gpa_filtered.tsv                    | Genes found to be associated with test phenotype                                                                                                                                                                               |
| gpa_patterns.txt                    |                                                                                                                                                                                                                                |
| gpa_sample.faa                      |                                                                                                                                                                                                                                |
| gpa_summary.tsv                     |                                                                                                                                                                                                                                |
| gpa.png, rare.png, unitigs.png      | Q-Q plot for gene presence/absence, rare variants, and unitigs. Assesses the distribution of obseved p-values with the expected<br>distribution under the null hypothesis of the test statistics.                              |
| gpa.tsv                             | Tested genes                                                                                                                                                                                                                   |
| heritability_all.tsv                | Information about heritability. Which gives information about what proportion of the phenotypic variation can be<br>explained by the genetic variants. Contains information about heritability for both variants and lineages. |
| heritability_lineages.tsv           |                                                                                                                                                                                                                                |
| heritability.ci.tsv                 |                                                                                                                                                                                                                                |
| heritability.tsv                    |                                                                                                                                                                                                                                |
| mapped_all.tsv                      | All unitigs mapped backed to the reference genome(s)                                                                                                                                                                           |
| mapped.tsv                          | Unitigs passing association threshold mapped to tested genomes                                                                                                                                                                 |
| panfeed_annotated_kmers.tsv         |                                                                                                                                                                                                                                |
| panfeed_annotated_kmers.tsv.gz      |                                                                                                                                                                                                                                |
| panfeed_clusters.txt                |                                                                                                                                                                                                                                |
| panfeed_filtered.tsv                |                                                                                                                                                                                                                                |
| panfeed_patterns.txt                |                                                                                                                                                                                                                                |
| panfeed_second_pass                 |                                                                                                                                                                                                                                |
| panfeed_targets.txt                 | List of samples used as inputs in panfeed.                                                                                                                                                                                     |
| panfeed.tsv                         | Associations from all tested kmers generated from panfeed.                                                                                                                                                                     |
| rare_filtered.tsv                   |                                                                                                                                                                                                                                |
| rare_patterns.txt                   |                                                                                                                                                                                                                                |
| rare_sample.faa                     |                                                                                                                                                                                                                                |
| rare_summary.emapper.annotations    |                                                                                                                                                                                                                                |
| rare_summary.emapper.hits           |                                                                                                                                                                                                                                |
| rare_summary.emapper.seed_orthologs |                                                                                                                                                                                                                                |
| rare_summary.tsv                    |                                                                                                                                                                                                                                |
| rare.tsv                            | Contains variants found to be significantly associated with the test phenotype                                                                                                                                                 |
| sample.faa                          |                                                                                                                                                                                                                                |
| small.txt                           |                                                                                                                                                                                                                                |
| struct_filtered.tsv                 |                                                                                                                                                                                                                                |
| struct_patterns.txt                 |                                                                                                                                                                                                                                |
| struct.tsv                          |                                                                                                                                                                                                                                |
| summary.emapper.annotations         |                                                                                                                                                                                                                                |
| summary.emapper.hits                |                                                                                                                                                                                                                                |
| summary.emapper.seed_orthologs      |                                                                                                                                                                                                                                |
| summary.tsv                         |                                                                                                                                                                                                                                |
| unitigs_filtered.tsv                | Contains unitigs found to be significantly associated with the test phenotype                                                                                                                                                  |
| unitigs_lineage.txt                 |                                                                                                                                                                                                                                |
| unitigs_patterns.txt                |                                                                                                                                                                                                                                |
| unitigs.tsv                         | List of all tested unitigs                                                                                                                                                                                                     |


## Testing

We have included a small dataset in order to test the pipeline in reasonable time
and resources. In its current state continuous integration (CI) in the cloud is not feasible
because certain rules require significant time and resources to complete (`annotate_reference`,
`get_snps`). Some workarounds might be added in the future to bypass those rules. In the meantime the
tests can be run on a decent laptop with 8 cores and at least ~10Gb RAM in a few hours.

The test dataset has been created from that [used in a mouse model of bloodstream infection]().

To run the tests, prepare a symbolic link to the eggnog-mapper
databases (as explained above), then do the following:

    cd test
    bash run_tests.sh

The script will prepare the input files, run the bootstrapping script, then run snakemake twice,
first in "dry" mode, and then "for real".

Please note that the only rule that is not tested is the one estimating lineages (`lineage_st`), as the
test dataset is a reduced part of the E. coli genome.

## TODO

- [x] Add the ability to use covariates in the associations
- [ ] manhattan_plot.py : handle cases in which the reference genome has more than one chromosome (either because it has plasmids or because it is a draft genome) ([enhancement issue](https://github.com/microbial-pangenomes-lab/gwas_template/issues/8))
- [ ] Easily switch to poppunk for lineage computation
- [ ] Combine all annotations in a series of webpages ([enhancement issue](https://github.com/microbial-pangenomes-lab/gwas_template/issues/6))
- [ ] Add references to the tools used in the pipeline ([documentation issue](https://github.com/microbial-pangenomes-lab/gwas_template/issues/7))
- [x] Use random file names for things that go in `/tmp` to avoid conflicts
- [ ] Use `/tmp` directories (as implemented by snakemake) to be efficient in I/O heavy rules
- [ ] Delete everything but the necessary files upon completion of a rule
    - [x] snippy
    - [x] panaroo
- [x] Avoid rules that list each input file as it might eventually become too long (including the current use of the `data/fastas` and `data/gffs` directories)
- [ ] Run QC on phenotypic data/genomes as part of bootstrapping
- [ ] Use snakemake resources system to budget memory requirements ([enhancement issue](https://github.com/microbial-pangenomes-lab/gwas_template/issues/9))
- [x] Swap sift4g for [more modern alternatives](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02948-3) ([enhancement issue](https://github.com/microbial-pangenomes-lab/gwas_template/issues/10))
- [x] Create a minimal test set that yields some hits and runs in reasonable time (~300 Ecoli dataset from BSI mouse model)
- [x] Also generate panfeed plots, and annotate its results
- [x] Harden panfeed rules against stochastic gzip file corruption ([fixed here](https://github.com/microbial-pangenomes-lab/gwas_template/pull/1))
- [ ] Swap `unitig-counter` for `bifrost` or `cuttlefish` ([enhancement issue](https://github.com/microbial-pangenomes-lab/gwas_template/issues/11))
- [ ] Heritability estimates using different distributions (i.e. for binary phenotypes the normal distribution is likely not appropriate?)
- [x] Add [abritamr](https://github.com/MDU-PHL/abritamr) to detect known AMR/VAGs - necessary for this pipeline???
- [ ] Add txt file that describes outputs produced from running the pipeline (in progress)
- [ ] Add documentation using something like read the docs

## Reference

TBD

## Author

Marco Galardini (marco.galardini@twincore.de)
