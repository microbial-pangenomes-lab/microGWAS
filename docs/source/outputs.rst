Outputs
=======

General output folder structure
-------------------------------

Running the suggested pipeline rules (``annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree``)
will yield the following
directory strcture in the ``out`` outputs folder:

..  code-block:: console

    out
    |____abritamr
    |____associations
    | |____phenotype
    | | |____panfeed_plots
    | |____inputs
    | | |____phenotype
    |____panfeed
    |____snps
    | |____unet
    |____wg
    | |____phenotype
    | |____inputs
    | | |____phenotype
    |____logs
    |____panaroo
    |____unitigs

Which correspond to:

* ``abritamr``: contains the predicted virulence associated genes (VAGs) and antimicrobial resistance gene (ARGs) for each sample
* ``logs``: contains the log files generated during the execution of each rule by snakemake, and can be used to inspect errors

**please describe the other folders using the same format as these examples.
make sure to note that if multiple phenotypes are defined in the config file,
then there will be multiple folders in ``associations`` and ``wg``**

Output files
------------

The above directories will contain the following files:

..  code-block:: console

    out
    |____abritamr
    | |____abritamr.txt
    | |____summary_virulence.txt
    | |____summary_partials.txt
    | |____summary_matches.txt

The virulence associated genes (VAGs) will be listed in the ``summary_virulence.txt`` file,
while the antimicrobial resistance genes (ARGs) will be listed in the ``summary_matches.txt`` file.

..  code-block:: console

    out
    |____associations
    | |____phenotype
    | | |____GO_gpa.png
    | | |____GO_rare.tsv
    | | |____GO_panfeed.png
    | | |____COG_rare.tsv
    | | |____GO_panfeed.tsv
    | | |____manhattan.png
    | | |____KEGG.tsv
    | | |____unitigs_filtered.tsv
    | | |____KEGG_rare.tsv
    | | |____heritability_all.tsv
    | | |____COG_gpa.png
    | | |____GO.png
    | | |____annotated_gpa_summary.tsv
    | | |____gpa.tsv
    | | |____COG.tsv
    | | |____panfeed_filtered.tsv
    | | |____KEGG_panfeed.tsv
    | | |____KEGG.png
    | | |____qq_rare.png
    | | |____COG_panfeed.tsv
    | | |____COG_panfeed.png
    | | |____panfeed_plots
    | | | |____sequence_btuD~~~irtA.png
    | | | |____significance_dltA~~~mbtB~~~irp2.png
    | | | |____sequence_legend.png
    | | | |____hybrid_dhbE.png
    | | |____unitigs.tsv
    | | |____GO_rare.png
    | | |____qq_gpa.png
    | | |____qq_unitigs.png
    | | |____panfeed.tsv
    | | |____rare_filtered.tsv
    | | |____mapped.tsv
    | | |____GO.tsv
    | | |____annotated_rare_summary.tsv
    | | |____KEGG_panfeed.png
    | | |____panfeed_annotated_kmers.tsv.gz
    | | |____COG_gpa.tsv
    | | |____KEGG_rare.png
    | | |____COG.png
    | | |____struct_filtered.tsv
    | | |____unitigs_patterns.txt
    | | |____rare.tsv
    | | |____GO_gpa.tsv
    | | |____gpa_filtered.tsv
    | | |____gpa_patterns.txt
    | | |____KEGG_gpa.tsv
    | | |____mapped_all.tsv
    | | |____unitigs_lineage.txt
    | | |____COG_rare.png
    | | |____annotated_panfeed_summary.tsv
    | | |____struct.tsv
    | | |____KEGG_gpa.png
    | | |____annotated_summary.tsv
    | |____inputs
    | | |____phenotype
    | | | |____phenotypes.tsv
    | | | |____similarity.tsv
    | | | |____distances.tsv
    | | | |____lineages_covariance.tsv
    | | | |____lineages.tsv

**The folder above is the most complex and most important, as the main results
from the associations go there. It might be worth it to lump together the files
that follow the convention {enrichment set}_{type of association}.{extension},
so that the list becomes shorter. Also it would be best to sort the files,
either alphabetically or by "type". For the ``panfeed_plots`` folder I have left
three example files, but the names are irrelevant**

..  code-block:: console

    out
    |____panfeed
    | |____kmers_to_hashes.tsv
    | |____kmers.tsv
    | |____hashes_to_patterns.tsv
    
..  code-block:: console

    out
    |____similarity.tsv
    |____distances.tsv
    |____annotated_reference.tsv
    
..  code-block:: console

    out
    |____snps
    | |____rare.vcf.gz
    | |____unet
    | | |____PROTEIN_ID_1.tsv.gz
    | | |____PROTEIN_ID_2.tsv.gz
    | | |____[...]
    
..  code-block:: console

    out
    |____wg
    | |____phenotype
    | | |____annotated_summary_lasso.tsv
    | | |____KEGG_ridge.png
    | | |____GO_ridge.tsv
    | | |____ridge.pkl
    | | |____COG_ridge.tsv
    | | |____ridge.txt
    | | |____GO_lasso.png
    | | |____KEGG_lasso.tsv
    | | |____KEGG_ridge.tsv
    | | |____KEGG_lasso.png
    | | |____mapped_lasso.tsv
    | | |____lasso.pkl
    | | |____mapped_ridge.tsv
    | | |____annotated_summary_ridge.tsv
    | | |____GO_lasso.tsv
    | | |____lasso.tsv
    | | |____lasso.txt
    | | |____GO_ridge.png
    | | |____ridge.tsv
    | | |____COG_lasso.png
    | | |____COG_ridge.png
    | | |____COG_lasso.tsv
    | |____inputs
    | | |____phenotype
    | | | |____phenotypes.tsv
    | | | |____variants.pkl
    | | | |____similarity.tsv
    | | | |____distances.tsv
    | | | |____variants.npz
    | | | |____lineages.tsv
    
..  code-block:: console

    out
    |____panaroo
    | |____core_gene_alignment.vcf.gz
    | |____core_gene_alignment.aln.treefile
    | |____gene_presence_absence.Rtab
    | |____gene_presence_absence.csv
    | |____core_gene_alignment.vcf.gz.csi
    | |____struct_presence_absence.Rtab
    | |____core_gene_alignment.aln
    
..  code-block:: console

    out
    |____unitigs
    | |____unitigs.unique_rows.Rtab.gz
    | |____unitigs.unique_rows_to_all_rows.txt
    | |____unitigs.txt.gz
