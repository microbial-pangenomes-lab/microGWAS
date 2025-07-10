# microGWAS: Bacterial Genome-Wide Association Studies

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12685497.svg)](https://doi.org/10.5281/zenodo.12685497)
[![Documentation Status](https://readthedocs.org/projects/microgwas/badge/?version=latest)](https://microgwas.readthedocs.io/en/latest/?badge=latest)

A comprehensive Snakemake pipeline for conducting bacterial genome-wide association studies (GWAS) on assembled genomes. microGWAS supports multiple phenotypes and provides extensive downstream analyses including functional annotation, enrichment analysis, and visualization.

## Key Features

For each phenotype, the pipeline runs associations using 6 complementary approaches:

- **Individual unitigs** - High-resolution genetic variants
- **Gene presence/absence** - Pangenome-based associations  
- **Rare variants** - Gene burden testing for low-frequency variants
- **Common variants** - SNP-based associations called against a reference genome
- **Gene cluster k-mers** - Locus-specific associations
- **Whole genome ML** - Combined unitig modeling

Additional analyses include:
- Heritability estimation using lineage and unitig data
- Functional enrichment analysis
- Manhattan plots and QQ plots
- Optional phylogenetic tree construction
- AMR/virulence gene prediction

## Getting Started

📖 **For complete instructions, visit the documentation:**

**[https://microgwas.readthedocs.io/](https://microgwas.readthedocs.io/)**

## Documentation

- **[Installation Guide](https://microgwas.readthedocs.io/en/latest/usage.html#installation)**
- **[Usage Instructions](https://microgwas.readthedocs.io/en/latest/usage.html)**
- **[Beginner's Tutorial](https://microgwas.readthedocs.io/en/latest/tutorials.html)**
- **[Input Requirements](https://microgwas.readthedocs.io/en/latest/inputs.html)**
- **[Output Description](https://microgwas.readthedocs.io/en/latest/outputs.html)**
- **[Testing](https://microgwas.readthedocs.io/en/latest/usage.html#testing)**

## TODO

- [ ] manhattan_plot.py : handle cases in which the reference genome has more than one chromosome (either because it has plasmids or because it is a draft genome) ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/8))
- [ ] Easily switch to poppunk for lineage computation
- [ ] Combine all annotations in a series of webpages ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/6))
- [ ] Use `/tmp` directories (as implemented by snakemake) to be efficient in I/O heavy rules
- [ ] Run QC on phenotypic data/genomes as part of bootstrapping
- [ ] Use snakemake resources system to budget memory requirements ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/9))
- [ ] Swap `unitig-counter` for `bifrost` or `cuttlefish` ([enhancement issue](https://github.com/microbial-pangenomes-lab/microGWAS/issues/11))
- [ ] Heritability estimates using different distributions (i.e. for binary phenotypes the normal distribution is likely not appropriate?)
- [ ] Add script to check for duplicated contigs during the bootstrap
- [ ] Swap panaroo for ggCaller, which would also allow for the use of raw reads


## Reference

[Burgaya, J., Damaris, B. F., Fiebig, J., & Galardini, M. (2025). microGWAS: A computational pipeline to perform large-scale bacterial genome-wide association studies. *Microbial Genomics*, 11(2), 001349.](https://www.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.001349)

## Citation

If you use microGWAS in your research, please cite the paper above and include the version DOI from Zenodo.

## Authors

Marco Galardini, Judit Burgaya, Bamu F. Damaris, Jenny Fiebig
