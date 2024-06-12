Rules
=====

The pipeline contains the following endpoint rules:

..  code-block:: console

    unitigs
    lineage_st
    find_amr_vag
    pangenome
    tree
    combine_heritability
    pyseer
    pyseer_rare
    wg
    qq_plots
    map_back
    manhattan_plots
    annotate_summary
    enrichment
    enrichment_plots
    panfeed

Which accomplish the following functions:

* ``unitigs``: will generate a variant set from the input samples based on a "global" de Brujin graph.
* ``lineage_st``: will generate a tab-separated file with the predicted sequence types (STs).
* ``find_amr_vag``: will generate a summary file with the predicted antimicrobial resistance genes identified into functionally relevant groups, and a summary file with the predicted virulence associated genes.
* ``pangenome``: will create mutliple output files:

    * ``pangenome``: gene_presence_absence.Rtab
    * ``pangenome_csv``: gene_presence_absence.csv
    * ``pangenome_genes``: gene_data.csv
    * ``structural``: struct_presence_absence.Rtab
    * ``core_genome_aln``: core_gene_alignment.aln
* ``tree``: will generate a tree file from the core genome alignment output from panaroo.
* ``combine_heritability``: will generate a file with the comined heritabilities: built from the lineages of each strain and by using a kinship matrix built from the unitigs presence and absence matrix.
* ``pyseer``: will test for associations of each unitig and the phenotype.
* ``pyseer_rare``: will test for rare variants based on the predicted protein coding variants from the sequence_unet rule.
* ``wg``: will test for locus effects using the presence/absence patterns of all unitigs.
* ``qq_plots``: will createa Q-Q plot to check that p-values are not inflated (large ‘shelves’ are symptomatic of poorly controlled confounding population structure)
* ``map_back``: will map back the associated genetic variants to the provided reference genomes.
* ``manhattan_plots``: will generate a Manhattan plot of the associated variant and the genome position.
* ``annotate_summary``: Will generate an annotated summary of the associated variants, including: mapped gene, number of strains, number of unitigs mapping back, avg-lrt-pvalue, COG/GO/KEGG category. 
* ``enrichment``: Will generate a file with the functional enrichment of the associated variants for GO terms, COG categories and KEGG pathways.
* ``enrichment_plots``: Will generate the plots from the previous rule.
* ``panfeed``: Will run panfeed to test gene cluster specific k-mers and produce output plots.


..  tip::

    Please note that some of the above rules will depend on each other.

**Here we could put figure 1 with the simplified DAG derived from snakemake**
