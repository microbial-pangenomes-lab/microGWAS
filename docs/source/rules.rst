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

* ``unitigs``: will generate a variant set from the input samples based on a "global" de Brujin graph

**Etcetera, you get the idea.**

..  tip::

    Please note that some of the above rules will depend on each other.

**Here we could put figure 1 with the simplified DAG derived from snakemake**
