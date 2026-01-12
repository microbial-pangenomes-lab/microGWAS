Rules
=====

The pipeline contains the following endpoint rules:

..  code-block:: console

    pangenome
    annotate_pangenome
    lineage_st
    find_amr_vag
    tree
    unitigs
    panfeed
    combine_heritability
    pyseer
    pyseer_rare
    wg
    wg_metrics
    map_back
    qq_plots
    manhattan_plots
    enrichment
    enrichment_plots
    annotate_summary

Which accomplish the following functions:

* ``unitigs``: will generate a variant set from the input samples based on a "global" de Brujin graph.
* ``lineage_st``: will generate a tab-separated file with the predicted sequence types (STs).
* ``find_amr_vag``: will generate a summary file with the predicted antimicrobial resistance genes identified into functionally relevant groups, and a summary file with the predicted virulence associated genes.
* ``pangenome``: will find the orthologous gene clusters across all samples and the chosen references
* ``annotate_pangenome``: will generate functional annotations for the pangenome using eggnog-mapper, including COG categories, GO terms, and KEGG pathway mappings.
* ``tree``: will generate a phylogenetic tree from the core genome alignment output from panaroo.
* ``combine_heritability``: will generate a file with the comined heritabilities: built from the lineages of each strain and by using a kinship matrix built from the unitigs presence and absence matrix.
* ``pyseer``: will test for associations of each unitig and the phenotype, as well as gene presence/absence patterns and lineage effects.
* ``pyseer_rare``: will test for rare variants based on the predicted deleterious protein coding variants.
* ``panfeed``: will test gene-cluster specific k-mers for their association with the phenotype(s), and produce output plots.
* ``wg``: will train two machine learning models (lasso and a ridge elastic nets) based on the presence/absence patterns of all unitigs.
* ``wg_metrics``: will calculate prediction performance metrics for the machine learning models trained by the ``wg`` rule, providing quantitative assessment of model accuracy.
* ``qq_plots``: will createa Q-Q plot to check that p-values are not inflated (large ‘shelves’ are symptomatic of poorly controlled confounding population structure)
* ``map_back``: will map back the associated genetic variants to the provided reference genomes.
* ``manhattan_plots``: will generate a Manhattan plot of the unitigs that map to the chosen reference genome.
* ``annotate_summary``: will generate an annotated summary table for all associations, including: the identity of the gene the variants map to, the number of strains, the average association pvalue, the gene ID across the selected reference genomes, and automatic annotations provided by ``eggnog-mapper``. 
* ``enrichment``: will generate a file with the functional enrichment of the associated variants for GO terms, COG categories and KEGG pathways.
* ``enrichment_plots``: will generate visualizations from the results of the ``enrichment`` rule.


..  tip::

    Please note that some of the above rules will depend on each other.

