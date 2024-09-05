Outputs
=======

General output folder structure
-------------------------------

Running the suggested pipeline rules (``annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree``)
will yield the following
directory strcture in the ``out`` outputs folder:

..  code-block:: console

    out
    |____associations
    | |____inputs
    | | |____phenotype
    | |____phenotype
    | | |____panfeed_plots
    |____wg
    | |____inputs
    | | |____phenotype
    | |____phenotype
    |____panfeed
    |____snps
    | |____unet
    |____panaroo
    |____unitigs
    |____abritamr
    |____logs

* ``associations``: contains the inputs and outputs for the locus and lineage associations, with one subfolder for each target phenotype

    * ``inputs``: contains the inputs for the associations
    * ``phenotype``: contains the association outputs, annotated summaries and functional enrichments
* ``wg``: contains the inputs and outputs for the whole genome associations, with one subfolder for each target phenotype

    * ``inputs``: contains the inputs for the whole genome associations
    * ``phenotype``: contains the associations output, annotated summaries and functional enrichmennts (for both lasso and ridge models)
* ``panfeed``: contains the input for the gene cluster specific k-mers associations
* ``snps``: contains the input for the rare variants associations

    * ``unet``: contains the estimated impact of all possible non-synonymous variants across the reference genome's proteome
* ``panaroo`` : contains the pangenome of all samples and references, as well as the core genome phylogenetic tree
* ``unitigs`` : contains the unitigs variant set based on a "global" de Brujin graph.
* ``abritamr``: contains the predicted virulence associated genes (VAGs) and antimicrobial resistance gene (ARGs) for each sample
* ``logs``: contains the log files generated during the execution of each rule by snakemake, which can be used to inspect errors

.. note::
    If multiple phenotypes are defined in the config file, there will be multiple folders in ``associations`` and ``wg``.

Output files
------------

The above directories will contain the following files:

..  code-block:: console

    out
    |____abritamr
    | |____summary_virulence.txt
    | |____summary_matches.txt

The virulence associated genes (VAGs) will be listed in the ``summary_virulence.txt`` file
(under the column ``Virulence``),
while the antimicrobial resistance genes (ARGs) will be listed in the ``summary_matches.txt`` file,
with one column per antimicrobial "class".

..  code-block:: console

    out
    |____associations
    | |____inputs
    | | |____phenotype
    | | | |____distances.tsv
    | | | |____lineages.tsv
    | | | |____lineages_covariance.tsv
    | | | |____phenotypes.tsv
    | | | |____similarity.tsv
    | |____phenotype
    | | |____annotated_summary.tsv
    | | |____annotated_gpa_summary.tsv
    | | |____annotated_panfeed_summary.tsv
    | | |____annotated_rare_summary.tsv
    | | |____heritability_all.tsv
    | | |____unitigs_lineage.txt
    | | |____mapped.tsv
    | | |____mapped_all.tsv
    | | |____panfeed.tsv
    | | |____panfeed_filtered.tsv
    | | |____rare.tsv
    | | |____rare_filtered.tsv
    | | |____struct.tsv
    | | |____struct_filtered.tsv
    | | |____unitigs.tsv
    | | |____unitigs_filtered.tsv
    | | |____unitigs_patterns.txt
    | | |____gpa.tsv
    | | |____gpa_filtered.tsv
    | | |____manhattan.png
    | | |____qq_gpa.png
    | | |____qq_panfeed.png
    | | |____qq_rare.png
    | | |____qq_unitigs.png
    | | |____COG.png
    | | |____COG.tsv
    | | |____COG_gpa.png
    | | |____COG_gpa.tsv
    | | |____COG_panfeed.png
    | | |____COG_panfeed.tsv
    | | |____COG_rare.png
    | | |____COG_rare.tsv
    | | |____GO.png
    | | |____GO.tsv
    | | |____GO_gpa.png
    | | |____GO_gpa.tsv
    | | |____GO_panfeed.png
    | | |____GO_panfeed.tsv
    | | |____GO_rare.png
    | | |____GO_rare.tsv
    | | |____KEGG.png
    | | |____KEGG.tsv
    | | |____KEGG_gpa.png
    | | |____KEGG_gpa.tsv
    | | |____KEGG_panfeed.png
    | | |____KEGG_panfeed.tsv
    | | |____KEGG_rare.png
    | | |____KEGG_rare.tsv
    | | |____panfeed_annotated_kmers.tsv.gz
    | | |____panfeed_plots
    | | | |____hybrid_GENE.png
    | | | |____sequence_GENE.png
    | | | |____significance_GENE.png
    | | | |____sequence_legend.png

* ``inputs`` folder: the ``distances.tsv``, ``linages.tsv``, ``lineages_covariance.tsv``, ``phenotypes.tsv``, and ``similarity.tsv`` files contain the association inputs for each target phenotype, so that they only contain the samples for which the phenotypic data is available 
* ``annotated_*.tsv``: contains the annotations of genes to which variants passing the association threshold map to; each row contains a gene, followed by the average associations' summary statistics, the frequency of the gene in the pangenome, the locus tag and gene name of the gene if it's encoded in the chosen reference(s), and finally the annotations given by ``eggnog-maper``, including COGs, GO terms and KEGG annotations
* ``heritability_all.tsv``: contains information about what proportion of the phenotypic variation can be explained by either the lineage membership or the genetic variants. The `genetics` column indicates the likelihood model used for the heritability estimation, `lik` the likelihood model used for the heritability estimation, `h2`, the proportion of phenotypic variance explained by the genetic effects. 
* ``unitigs_lineage.txt``: lineage associations output; for each lineage the association p-value is reported; the name is misleading, as the unitigs presence/absence patterns have not been used for this association tests
* ``mapped.tsv``: mapping information on the unitigs passing the association threshold, across all samples and reference(s)
* ``mapped_all.tsv``: mapping information for all tested unitigs to the reference genome(s)
* ``panfeed.tsv``, ``rare.tsv``, ``struct.tsv``, ``unitigs.tsv``, and ``gpa.tsv``: contain the raw association results as given by ``pyseer``, with one file per variant set
* * ``panfeed_filtered.tsv``, ``rare_filtered.tsv``, ``struct_filtered.tsv``, ``unitigs_filtered.tsv``, and ``gpa_filtered.tsv``: contain the variants passing the association threshold
* ``manhattan.png``: manhattan plot for all unitigs mapping to the main reference genome
* ``qq_*.png``: QQ plot to assess the distribution of observed p-values with the expected distribution under the null hypothesis of the test statistics
* ``COG_*.tsv``, ``GO_*.tsv``, and ``KEGG_*.tsv``: functional enrichment tests results for each variant set
* ``COG_*.png``, ``GO_*.png``, and ``KEGG_*.png``: plots to visualise the results of the functional enrichment tests
* ``panfeed_annotated_kmers.tsv.gz``: detailed annotation of all k-mers mapping to associated gene clusters, as given by ``panfeed``
* ``panfeed_plots``: visualizaion of the gene-cluster specific k-mers, with 3 files for each associated gene cluster, as given by ``panfeed``

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
* ``annotated_reference.tsv`` is the functional annotation of the reference using ``eggnog-mapper``. It provides mappings to COG categories, KEGG terms, pathways and more. 

..  code-block:: console

    out
    |____snps
    | |____rare.vcf.gz
    | |____unet
    | | |____PROTEIN_ID_1.tsv.gz
    | | |____PROTEIN_ID_2.tsv.gz
    | | |____[...]
    
* ``rare.vcf.gz``: all rare deleterious variants identified across all samples merged into a single VCF file. 
* ``unet``: this directory contains, for each protein sequence encoded in the reference genome, the estimated impact of every possible non-synonymous variants. The ``pred`` column indicates the probability that a variant is deleterious; the pipeline uses a threshold of 0.5.  

..  code-block:: console

    out
    |____inputs
    | |____phenotype
    | | |____distances.tsv
    | | |____lineages.tsv
    | | |____phenotypes.tsv
    | | |____similarity.tsv
    | | |____variants.npz
    | | |____variants.pkl
    |____wg
    | |____phenotype
    | | |____annotated_summary_lasso.tsv
    | | |____annotated_summary_ridge.tsv
    | | |____COG_lasso.png
    | | |____COG_lasso.tsv
    | | |____COG_ridge.png
    | | |____COG_ridge.tsv
    | | |____GO_lasso.png
    | | |____GO_lasso.tsv
    | | |____GO_ridge.png
    | | |____GO_ridge.tsv
    | | |____KEGG_lasso.png
    | | |____KEGG_lasso.tsv
    | | |____KEGG_ridge.png
    | | |____KEGG_ridge.tsv
    | | |____lasso.pkl
    | | |____lasso.tsv
    | | |____lasso.txt
    | | |____mapped_lasso.tsv
    | | |____mapped_ridge.tsv
    | | |____ridge.pkl
    | | |____ridge.tsv
    | | |____ridge.txt    
    
The contents of the ``wg`` are very similar to the equivalent files in the ``associations`` folder. The differences are:

* in the ``inputs`` subfolder: ``variants.*`` are the ``pyseer`` checkpoint files to avoid loading the full set of unitigsmultiple times 
* ``lasso.tsv``: association output between each unitig and the phenotype; based on the lasso model 
* ``lasso.txt``: the table shows the prediction perfomance of the lasso model; the size represents the number of samples, R2 the model performance and the True and False predictions for each lineage
* ``ridge.tsv``: association output between each unitig and the phenotype; based on the ridge model
* ``ridge.txt``: the table shows the prediction perfomance of the ridge model; the size represents the number of samples, R2 the model performance and the True and False predictions
* ``lasso.pkl`` and ``ridge.pkl``: ``pyseer`` checkpoint file containing the trained machine learning model, which can be used to predict the phenotype in new samples

..  code-block:: console

    out
    |____panaroo
    | |____gene_presence_absence.Rtab
    | |____gene_presence_absence.csv
    | |____struct_presence_absence.Rtab
    | |____core_gene_alignment.aln
    | |____core_gene_alignment.aln.treefile
    | |____core_gene_alignment.vcf.gz
      
* ``gene_presence_absence.Rtab``: gene clusters binary presence/absence file: for each orthologous gene identified by panaroo, its presence (1) and absence (0) is reported for all samples and the selected references 
* ``gene_presence_absence.csv``: describes which gene clusters are present in which samples, and if so, it provides the gene IDs/locus tags; paralogs are separated by the ``;`` character 
* ``struct_presence_absence.Rtab``: gene ordering variants presence/absence file, with the involved genes enlisted in the first column, separated with the ``-`` character 
* ``core_gene_alignment.aln``: contains the core genome alignment generated through the concatenation of the alignment of each gene
* ``core_gene_alignment.aln.treefile``: contains a phylogenetic tree constructed from the core genome alignment file ``core_gene_alignment.aln``  
* ``core_gene_alignment.vcf.gz``: contains the core genome alignment in VCF format


..  code-block:: console

    out
    |____unitigs
    | |____unitigs.unique_rows.Rtab.gz
    | |____unitigs.unique_rows_to_all_rows.txt
    | |____unitigs.txt.gz

* ``unitigs.unique_rows.Rtab.gz``: contains the unique unitig patterns found across the input genomes. The number of lines represents the number of unique tests that need to be corrected for in the association analysis
* ``unitigs.unique_rows_to_all_rows.txt``:  provides information on the mapping from the unique unitig patterns to all instances of those patterns observed across the input genomes
* ``unitigs.txt.gz``: contains the list of unitigs counted across the input genomes and which samples encode for them
