Rules
=====

The pipeline contains the following endpoint rules:

..  code-block:: console

    ggcaller
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
    annotate_summary [cite: 266]

Which accomplish the following functions:

* ``ggcaller``: will generate GFF annotations for all sample genomes using ggCaller, providing gene predictions and functional annotations. [cite: 266, 267] If pre-computed GFF files are specified via the input table, this rule will instead validate the user-provided paths and skip the time-consuming *de novo* gene calling step. [cite: 267]
* ``unitigs``: will generate a variant set from the input samples based on a "global" de Brujin graph. [cite: 269]
* ``lineage_st``: will generate a tab-separated file with the predicted sequence types (STs). [cite: 270]
* ``find_amr_vag``: will generate a summary file with the predicted antimicrobial resistance genes identified into functionally relevant groups, and a summary file with the predicted virulence associated genes. [cite: 271]
* ``pangenome``: will find the orthologous gene clusters across all samples and the chosen references using panaroo. [cite: 272]
* ``annotate_pangenome``: will generate functional annotations for the pangenome using eggnog-mapper, including COG categories, GO terms, and KEGG pathway mappings. [cite: 273]
* ``tree``: will generate a phylogenetic tree from the core genome alignment output from panaroo. [cite: 274]
* ``combine_heritability``: will generate a file with the comined heritabilities: built from the lineages of each strain and by using a kinship matrix built from the unitigs presence and absence matrix. [cite: 275]
* ``pyseer``: will test for associations of each unitig and the phenotype, as well as gene presence/absence patterns and lineage effects. [cite: 276]
* ``pyseer_rare``: will test for rare variants based on the predicted deleterious protein coding variants. [cite: 277]
* ``panfeed``: will test gene-cluster specific k-mers for their association with the phenotype(s), and produce output plots. [cite: 278]
* ``wg``: will train two machine learning models (lasso and a ridge elastic nets) based on the presence/absence patterns of all unitigs. [cite: 279]
* ``wg_metrics``: will calculate prediction performance metrics for the machine learning models trained by the ``wg`` rule, providing quantitative assessment of model accuracy. [cite: 280]
* ``qq_plots``: will createa Q-Q plot to check that p-values are not inflated (large ‘shelves’ are symptomatic of poorly controlled confounding population structure) [cite: 281]
* ``map_back``: will map back the associated genetic variants to the provided reference genomes. [cite: 281]
* ``manhattan_plots``: will generate a Manhattan plot of the unitigs that map to the chosen reference genome. [cite: 282]
* ``annotate_summary``: will generate an annotated summary table for all associations, including: the identity of the gene the variants map to, the number of strains, the average association pvalue, the gene ID across the selected reference genomes, and automatic annotations provided by ``eggnog-mapper``. [cite: 283]
* ``enrichment``: will generate a file with the functional enrichment of the associated variants for GO terms, COG categories and KEGG pathways. [cite: 284]
* ``enrichment_plots``: will generate visualizations from the results of the ``enrichment`` rule. [cite: 285]

..  tip::

    Please note that some of the above rules will depend on each other. [cite: 286]
