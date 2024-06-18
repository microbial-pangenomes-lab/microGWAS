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

* ``abritamr``: contains the predicted virulence associated genes (VAGs) and antimicrobial resistance gene (ARGs) for each sample.
* ``associations``:

    * ``phenotype``: contains the output associations, annotated summaries and functional enrichments for the target phenotype.
    * ``inputs``: contains the inputs for the associations.
* ``panfeed``: contains the input for the gene cluster specific k-mers assocaitions.
* ``snps``: contains the input for the rare variants assocaitions.
* ``wg``:

    * ``phenotype``: contains the output associations, annotated summaries and functional enrichmennts for the target phenotype for the whole genome model (for both lasso and ridge models).
    * ``inputs``: contains the inputs for the whole genome model associations.
* ``logs``: contains the log files generated during the execution of each rule by snakemake, and can be used to inspect errors
* ``panaroo`` : contains the generated outputs from panaroo. You will also find the generated phylogenetic tree in this directory.
* ``unitigs`` : contains a variant set from the input samples based on a "global" de Brujin graph.

.. note::
    If multiple phenotypes are defined in the config file, there will be multiple folders in ``associations`` and ``wg``.

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

* ``annotated_*.tsv``: contains gene annotations. The rows are the genes, and the columns the COG name, category, GO ids and KEGG terms and other description partaining to the genes. 
* ``COG_*.tsv``: files with results from COG analysis. Each row represents a COG category and the columns the category name, pvalue and adjusted pvalues (qvalue, emperical-qvalue).
* ``COG_*.png``: plots to visualise COG analysis.
* ``distances.tsv``: contains pairwise distances between samples. 
* ``GO_*.tsv``: files with GO terms .
* ``GO_*.png``: plots to visualise GO terms.
* ``filtered_*.tsv``: associations filtered based on computed threshold  to contain only variants significantly associated with the test phenotype.
* ``heritability_*.tsv``: contains information about what proportion of the phenotypic variation can be explained by the genetic variants. Each row represents the phenotype or trait on which the analysis was conducted on. The `phenotype` column indicates the phenotype or trait being anlaysed, `genetics` column indicates the likelihood model used for the heritability estimation, `lik` the likelihood model used for the heritability estimation, `h2`, the proportion of phenotypic variance explained by the genetic effects. 
* ``lineages.tsv```: contains information about the lineages present in the samples. 
* ``lineages_covariance.tsv```: contains details on the covariances or correlations between the lineages present in the samples. 
* ``manhattan.png``: manhattan plot to visualise association results.
* ``mapped_all.tsv``: all unitigs mapped backed to the reference genome(s).
* ``mapped.tsv``: unitigs passing association threshold mapped to reference genome(s).
* ``KEGG_*.tsv``: files with results from KEGG analysis.
* ``KEGG_*.png``: plots to visualise KEGG analysis.
* ``panfeed_plots``: plots to visualise k-mers panfeed results (`might need to explain this better once I see what the plots look like`).
* ``qq_*.png``: qq plot to assess the distribution of observed p-values with the expected distribution under the null hypothesis of the test statistics. 
* ``similarity.tsv``: contains similarity matrix between samples. Used to account for relatedness between samples.
* ``struc.tsv``: 

..  code-block:: console

    out
    |____panfeed
    | |____kmers_to_hashes.tsv
    | |____kmers.tsv
    | |____hashes_to_patterns.tsv
    
* ``kmers_to_hashes.tsv``: file used to match gene clusters, k-mer sequences and the hash for the respective presence/absence pattern.
* ``kmers.tsv``:  k-mers metadata file
* ``hashes_to_patterns.tsv``: file contains binary presence/absence matrix for all unique k-mer patterns (rows) across samples (columns)

..  code-block:: console

    out
    |____similarity.tsv
    |____distances.tsv
    |____annotated_reference.tsv

* ``similarity.tsv`` and ``distances.tsv`` provides information about the genetic reletedness of the test strains. They are both used to account for population structure during the association analysis. 
* ``annotated_reference.tsv`` is the functional annotation of the reference using Eggnog. It provides mappings to COG categories, KEGG terms, pathways and more. 

..  code-block:: console

    out
    |____snps
    | |____rare.vcf.gz
    | |____unet
    | | |____PROTEIN_ID_1.tsv.gz
    | | |____PROTEIN_ID_2.tsv.gz
    | | |____[...]
    
* ``rare.vcf.gz``: all rare variants merged into a single file. 
* ``unet``: this directory contains the snp information for each strain.  

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
    
* ``annotated_*.tsv``: contains gene annotations as previously described.  
* ``COG_*.tsv``: files with results from COG analysis as previously described.
* ``COG_*.png``: plots to visualise COG analysis
* ``GO_*.tsv``: files with GO terms 
* ``GO_*.png``: plots to visualise GO terms
* ``KEGG_*.tsv``: files with results from KEGG analysis
* ``KEGG_*.png``: plots to visualise KEGG analysis
* ``lasso.tsv``: association output between each unitig and the phenotype. Based on lasso model. 
* ``lasso.txt``: the table shows the prediction perfomance of the lasso model. The size represents the number of samples, R2 the model performance and the True and False predictions. 
* ``lasso.pkl``
* ``mapped_*.tsv``: all unitigs mapped backed to the reference genome(s). 
* ``ridge.tsv``: association output between each unitig and the phenotype. Based on the ridge model. 
* ``ridge.txt``: the table shows the prediction perfomance of the ridge model. The size represents the number of samples, R2 the model performance and the True and False predictions. 
* ``ridge.pkl``: 

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
      
* ``core_gene_alignment.vcf.gz``: file containing the variants identified in the core genome alignment. This file allows one to examine the sequence variations within the core genes across the different samples. 
* ``core_gene_alignment.vcf.gz.csi``:  an index file associated with the `core_gene_alignment.vcf.gz` file. It aids the efficient access and querying of the compressed file. 
* ``core_gene_alignment.aln``: contains alignments of genes present in the fraction of genomes specified when running the `Panaroo` analysis.
* ``core_gene_alignment.aln.treefile``: contains a phylogenetic tree constructed from the core genome alignment file `core_gene_alignment.aln`. The tree file maybe visualized and analyzed using any tree viewing software.  
* ``gene_presence_absence.csv``: file describes which gene clusters are present in which samples. If the gene gene cluster is present in a sample, the sequence name of the representative sequence for the sample is given in the matrix. 
* ``gene_presence_absence.Rtab``: this is tab separated version of the `gene_presence_absence.csv` file. It binarises the gene presence and absence information in each sample. 
* ``struct_presence_absence.Rtab``: file details the presence and absence of various genomic rearrangements events, with the involved genes enlisted in the respective column headers. 


..  code-block:: console

    out
    |____unitigs
    | |____unitigs.unique_rows.Rtab.gz
    | |____unitigs.unique_rows_to_all_rows.txt
    | |____unitigs.txt.gz

* ``unitigs.unique_rows.Rtab.gz``: contains the unique unitig patterns found across the input genomes. The number of lines represents the number of unique tests that need to be corrected for in the association analysis.
* ``unitigs.unique_rows_to_all_rows.txt``:  provides information on the mapping from the unique unitig patterns to all instances of those patterns observed across the input genomes.
* ``unitigs.txt.gz``: file contains the list of unitigs counted across the input genomes.