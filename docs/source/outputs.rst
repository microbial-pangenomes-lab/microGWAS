Outputs
=======

General output folder structure
-------------------------------

Running the suggested pipeline rules (``annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree``) [cite: 178]
will yield the following
directory strcture in the ``out`` outputs folder: [cite: 178]

..  code-block:: console

    out
    |____associations
    |
    |____inputs [cite: 179]
    | | |____phenotype [cite: 179]
    | |____phenotype [cite: 179]
    | |
    | |____panfeed_plots [cite: 180]
    |____wg [cite: 180]
    | |____inputs [cite: 180]
    | |
    |____phenotype [cite: 181]
    | 
    |____phenotype [cite: 181]
    |____panfeed [cite: 181]
    |____snps [cite: 181]
    |
    |____unet [cite: 182]
    |____panaroo [cite: 182]
    |____unitigs [cite: 182]
    |____abritamr [cite: 182]
    |____logs [cite: 182]

* ``associations``: contains the inputs and outputs for the locus and lineage associations, with one subfolder for each target phenotype [cite: 182]

    * ``inputs``: contains the inputs for the associations [cite: 182]
    * ``phenotype``: contains the association outputs, annotated summaries and functional enrichments [cite: 182]
* ``wg``: contains the inputs and outputs for the whole genome associations, with one subfolder for each target phenotype [cite: 182]

    * ``inputs``: contains the inputs for the whole genome associations [cite: 182, 183]
    * ``phenotype``: contains the associations output, annotated summaries and functional enrichmennts (for both lasso and ridge models) [cite: 183]
* ``panfeed``: contains the input for the gene cluster specific k-mers associations [cite: 183]
* ``snps``: contains the input for the rare variants associations [cite: 183]

    * ``unet``: contains the estimated impact of all possible non-synonymous variants across the reference genome's proteome [cite: 183]
* ``panaroo`` : contains the pangenome of all samples and references, as well as the core genome phylogenetic tree [cite: 183]
* ``unitigs`` : contains the unitigs variant set based on a "global" de Brujin graph. [cite: 183, 184]
* ``abritamr``: contains the predicted virulence associated genes (VAGs) and antimicrobial resistance gene (ARGs) for each sample [cite: 184]
* ``logs``: contains the log files generated during the execution of each rule by snakemake, which can be used to inspect errors [cite: 184]

.. note::
    If multiple phenotypes are defined in the config file, there will be multiple folders in ``associations`` and ``wg``. [cite: 184]

Output files
------------

The above directories will contain the following files: [cite: 185]

..  code-block:: console

    out
    |____abritamr
    |
    |____summary_virulence.txt [cite: 186]
    | |____summary_matches.txt [cite: 186]

The virulence associated genes (VAGs) will be listed in the ``summary_virulence.txt`` file [cite: 186]
(under the column ``Virulence``), [cite: 186]
while the antimicrobial resistance genes (ARGs) will be listed in the ``summary_matches.txt`` file, [cite: 186]
with one column per antimicrobial "class". [cite: 186]

..  code-block:: console

    out
    |____associations
    |
    |____inputs [cite: 187, 188]
    | | |____phenotype [cite: 188]
    | | |
    |____distances.tsv [cite: 189]
    | | | 
    | | | |____lineages.tsv [cite: 189]
    | | |
    |____lineages_covariance.tsv [cite: 190]
    | | | |____phenotypes.tsv [cite: 190]
    | | 
    | |
    |____similarity.tsv [cite: 191]
    | |____phenotype [cite: 191]
    | | |____annotated_summary.tsv [cite: 191]
    | |
    | | |____annotated_gpa_summary.tsv [cite: 192]
    | | |____annotated_panfeed_summary.tsv [cite: 192]
    | |
    |____annotated_rare_summary.tsv [cite: 193]
    | | 
    | | |____annotated_vcf.tsv [cite: 193]
    | |
    |____heritability_all.tsv [cite: 194]
    | | |____unitigs_lineage.txt [cite: 194]
    | | 
    | |
    |____mapped.tsv [cite: 195]
    | | |____mapped_all.tsv [cite: 195]
    | | |____panfeed.tsv [cite: 195]
    |
    | 
    | | |____panfeed_filtered.tsv [cite: 196]
    | | |____rare.tsv [cite: 196]
    | |
    |____rare_filtered.tsv [cite: 197]
    | | 
    | | |____struct.tsv [cite: 197]
    | |
    |____struct_filtered.tsv [cite: 198]
    | | |____unitigs.tsv [cite: 198]
    | | 
    | |
    |____unitigs_filtered.tsv [cite: 199]
    | | |____unitigs_patterns.txt [cite: 199]
    | | |____vcf.tsv [cite: 199]
    |
    | 
    | | |____vcf_filtered.tsv [cite: 200]
    | | |____vcf_patterns.txt [cite: 200]
    | |
    |____gpa.tsv [cite: 201]
    | | 
    | | |____gpa_filtered.tsv [cite: 201]
    | |
    |____manhattan.png [cite: 202]
    | | |____qq_gpa.png [cite: 202]
    | | 
    | |
    |____qq_rare.png [cite: 203]
    | | |____qq_unitigs.png [cite: 203]
    | | |____COG.png [cite: 203]
    |
    | 
    | | |____COG.tsv [cite: 204]
    | | |____COG_gpa.png [cite: 204]
    | |
    |____COG_gpa.tsv [cite: 205]
    | | 
    | | |____COG_panfeed.png [cite: 205]
    | |
    |____COG_panfeed.tsv [cite: 206]
    | | |____COG_rare.png [cite: 206]
    | | 
    | |
    |____COG_rare.tsv [cite: 207]
    | | |____GO.png [cite: 207]
    | | |____GO.tsv [cite: 207]
    |
    | 
    | | |____GO_gpa.png [cite: 208]
    | | |____GO_gpa.tsv [cite: 208]
    | |
    |____GO_panfeed.png [cite: 209]
    | | 
    | | |____GO_panfeed.tsv [cite: 209]
    | |
    |____GO_rare.png [cite: 210]
    | | |____GO_rare.tsv [cite: 210]
    | | 
    | |
    |____KEGG.png [cite: 211]
    | | |____KEGG.tsv [cite: 211]
    | | |____KEGG_gpa.png [cite: 211]
    |
    | 
    | | |____KEGG_gpa.tsv [cite: 212]
    | | |____KEGG_panfeed.png [cite: 212]
    | |
    |____KEGG_panfeed.tsv [cite: 213]
    | | 
    | | |____KEGG_rare.png [cite: 213]
    | |
    |____KEGG_rare.tsv [cite: 214]
    | | |____panfeed_annotated_kmers.tsv.gz [cite: 214]
    | | 
    |
    |____panfeed_plots [cite: 215]
    | | | |____hybrid_GENE.png [cite: 215]
    | | |
    |____sequence_GENE.png [cite: 216]
    | | 
    | | | |____significance_GENE.png [cite: 216]
    | | |
    |____sequence_legend.png [cite: 217]

* ``inputs`` folder: the ``distances.tsv``, ``lineages.tsv``, ``lineages_covariance.tsv``, ``phenotypes.tsv``, and ``similarity.tsv`` files contain the association inputs for each target phenotype, so that they only contain the samples for which the phenotypic data is available [cite: 217]
* ``annotated_*.tsv``: contains the annotations of genes to which variants passing the association threshold map to; [cite: 217]
  each row contains a gene, followed by the average associations' summary statistics, the frequency of the gene in the pangenome, the locus tag and gene name of the gene if it's encoded in the chosen reference(s), and finally the annotations given by ``eggnog-mapper``, including COGs, GO terms and KEGG annotations. [cite: 218]
  ``annotated_vcf.tsv`` has a different format, since it reports individual short variants against the chosen reference along with their predicted effect [cite: 219]
* ``heritability_all.tsv``: contains information about what proportion of the phenotypic variation can be explained by either the lineage membership or the genetic variants. [cite: 219]
  The `genetics` column indicates the likelihood model used for the heritability estimation, `lik` the likelihood model used for the heritability estimation, `h2`, the proportion of phenotypic variance explained by the genetic effects. [cite: 220]
* ``unitigs_lineage.txt``: lineage associations output; for each lineage the association p-value is reported; [cite: 221]
  the name is misleading, as the unitigs presence/absence patterns have not been used for this association tests [cite: 222]
* ``mapped.tsv``: mapping information on the unitigs passing the association threshold, across all samples and reference(s) [cite: 222]
* ``mapped_all.tsv``: mapping information for all tested unitigs to the reference genome(s) [cite: 222]
* ``panfeed.tsv``, ``rare.tsv``, ``vcf.tsv``, ``struct.tsv``, ``unitigs.tsv``, and ``gpa.tsv``: contain the raw association results as given by ``pyseer``, with one file per variant set [cite: 222]
* ``panfeed_filtered.tsv``, ``rare_filtered.tsv``, ``vcf_filtered.tsv``, ``struct_filtered.tsv``, ``unitigs_filtered.tsv``, and ``gpa_filtered.tsv``: contain the variants passing the association threshold [cite: 222]
* ``manhattan.png``: manhattan plot for all unitigs mapping to the main reference genome [cite: 222]
* ``qq_*.png``: QQ plot [cite: 222]
  to assess the distribution of observed p-values with the expected distribution under the null hypothesis of the test statistics [cite: 223]
* ``COG_*.tsv``, ``GO_*.tsv``, and ``KEGG_*.tsv``: functional enrichment tests results for each variant set [cite: 223]
* ``COG_*.png``, ``GO_*.png``, and ``KEGG_*.png``: plots to visualise the results of the functional enrichment tests [cite: 223]
* ``panfeed_annotated_kmers.tsv.gz``: detailed annotation of all k-mers mapping to associated gene clusters, as given by ``panfeed`` [cite: 223]
* ``panfeed_plots``: visualizaion of the gene-cluster specific k-mers, with 3 files for each associated gene cluster, as given by ``panfeed`` [cite: 223]

..  code-block:: console

    out
    |____panfeed
    
    | [cite: 224]
    |____kmers_to_hashes.tsv [cite: 224]
    | |____kmers.tsv [cite: 224]
    |
    |____hashes_to_patterns.tsv [cite: 225]
    
* ``kmers_to_hashes.tsv``: file used to match gene clusters, k-mer sequences and the hash for the respective presence/absence pattern. [cite: 225]
* ``kmers.tsv``:  k-mers metadata file [cite: 226]
* ``hashes_to_patterns.tsv``: file contains binary presence/absence matrix for all unique k-mer patterns (rows) across samples (columns) [cite: 226]

..  code-block:: console

    out
    |____similarity.tsv
    |____distances.tsv
    |____annotated_reference.tsv 

* ``similarity.tsv`` and ``distances.tsv`` provides information about the genetic reletedness of the test strains. [cite: 226]
  They are both used to account for population structure during the association analysis. [cite: 227]
* ``annotated_reference.tsv`` is the functional annotation of the reference using ``eggnog-mapper``. [cite: 228]
  It provides mappings to COG categories, KEGG terms, pathways and more. [cite: 229]

..  code-block:: console

    out
    |____snps
    |
    |____common.vcf.gz [cite: 231]
    | |____rare.vcf.gz [cite: 231]
    | |____unet [cite: 231]
    | | 
    |
    |____PROTEIN_ID_1.tsv.gz [cite: 232]
    | | |____PROTEIN_ID_2.tsv.gz [cite: 232]
    | | 
    |
    |____[...] [cite: 233]
    
* ``common.vcf.gz``: all common short variants with respect to the chosen reference genome identified across all samples merged into a single VCF file. [cite: 233]
* ``rare.vcf.gz``: all rare deleterious variants identified across all samples merged into a single VCF file. [cite: 234]
* ``unet``: this directory contains, for each protein sequence encoded in the reference genome, the estimated impact of every possible non-synonymous variants. [cite: 235]
  The ``pred`` column indicates the probability that a variant is deleterious; the pipeline uses a threshold of 0.5. [cite: 236]

..  code-block:: console

    out
    |____inputs
    |
    |____phenotype [cite: 238]
    | | |____distances.tsv [cite: 238]
    | | |____lineages.tsv [cite: 238]
    |
    | 
    |____phenotypes.tsv [cite: 239]
    | | |____similarity.tsv [cite: 239]
    | |
    |____variants.npz [cite: 240]
    | | 
    |____variants.pkl [cite: 240]
    |____wg [cite: 240]
    |
    |____phenotype [cite: 241]
    | | |____annotated_summary_lasso.tsv [cite: 241]
    | 
    | |____annotated_summary_ridge.tsv [cite: 241]
    |
    | |____COG_lasso.png [cite: 242]
    | | |____COG_lasso.tsv [cite: 242]
    | |
    |____COG_ridge.png [cite: 243]
    | | |____COG_ridge.tsv [cite: 243]
    | | |____GO_lasso.png [cite: 243]
    |
    | 
    |____GO_lasso.tsv [cite: 244]
    | | |____GO_ridge.png [cite: 244]
    | |
    |____GO_ridge.tsv [cite: 245]
    | | 
    |____KEGG_lasso.png [cite: 245]
    | | |____KEGG_lasso.tsv [cite: 245]
    |
    | |____KEGG_ridge.png [cite: 246]
    | | 
    |____KEGG_ridge.tsv [cite: 246]
    | |
    |____lasso.pkl [cite: 247]
    | | |____lasso.tsv [cite: 247]
    | | 
    |____lasso_predictions.tsv [cite: 247]
    |
    | |____metrics_lasso.tsv [cite: 248]
    | | |____mapped_lasso.tsv [cite: 248]
    | |
    |____mapped_ridge.tsv [cite: 249]
    | | |____ridge.pkl [cite: 249]
    | | |____ridge.tsv [cite: 249]
    |
    | 
    |____ridge_predictions.tsv [cite: 250]    
    | |
    |____metrics_ridge.tsv [cite: 251]
    
The contents of the ``wg`` are very similar to the equivalent files in the ``associations`` folder. [cite: 251]
The differences are: [cite: 252]

* in the ``inputs subfolder``: ``variants.*`` are the ``pyseer`` checkpoint files to avoid loading the full set of unitigsmultiple times [cite: 252]
* ``lasso.tsv`` and ``ridge.tsv``: association output between each unitig and the phenotype [cite: 252]
* ``lasso_predictions.tsv`` and ``ridge_predictions.tsv``: table showing the true and predicted values for each sample [cite: 252]
* ``metrics_lasso.tsv`` and ``metrics_ridge.tsv``: model prediction performance metrics on the training set. [cite: 252]
  The actual metrics depend on whether the phenotype is binary or continuous [cite: 253]
* ``lasso.pkl`` and ``ridge.pkl``: ``pyseer`` checkpoint file containing the trained machine learning model, which can be used to predict the phenotype in new samples [cite: 253]

..  code-block:: console

    out
    |____ggcaller
    |
    |____gene_calls.faa [cite: 254]
    | |____gene_calls.ffn [cite: 254]
    | |____GFF [cite: 254]
    |
    |____ORF_dir [cite: 255]
    | 
    |____Path_dir [cite: 255]

.. note::
    If user-provided GFF files are specified via the input table (``use_user_gffs: true``), the pipeline completely circumvents de novo structural annotations and assembly processing. [cite: 255]
    As a result, the default `out/ggcaller/` internal pipeline folder outputs shown above will not be populated, except for manifest validation logs. [cite: 256]

* ``gene_calls.faa``: contains the predicted protein sequences [cite: 257]
* ``gene_calls.ffn``: contains the predicted nucleotide sequences [cite: 257]
* ``GFF``: contains the gene calling results in GFF format [cite: 257]
* ``ORF_dir``: contains the predicted open reading frames [cite: 257]
* ``Path_dir``: contains the predicted pathways [cite: 257]

..  code-block:: console

    out
    |____panaroo
    |
    |____gene_presence_absence.Rtab [cite: 258]
    | |____gene_presence_absence.csv [cite: 258]
    | |____struct_presence_absence.Rtab [cite: 258]
    |
    |____core_gene_alignment.aln [cite: 259]
    | 
    |____core_gene_alignment.aln.treefile [cite: 259]
    | |____core_gene_alignment.vcf.gz [cite: 259]
    |
    |____pangenome_sample.faa [cite: 260]
    | 
    |____pangenome.emapper.annotations [cite: 260]

* ``gene_presence_absence.Rtab``: gene clusters binary presence/absence file: for each orthologous gene identified by panaroo, its presence (1) and absence (0) is reported for all samples and the selected references [cite: 260]
* ``gene_presence_absence.csv``: describes which gene clusters are present in which samples, and if so, it provides the gene IDs/locus tags; [cite: 260]
  paralogs are separated by the ``;`` character [cite: 261]
* ``struct_presence_absence.Rtab``: gene ordering variants presence/absence file, with the involved genes enlisted in the first column, separated with the ``-`` character [cite: 261]
* ``core_gene_alignment.aln``: contains the core genome alignment generated through the concatenation of the alignment of each gene [cite: 261]
* ``core_gene_alignment.aln.treefile``: contains a phylogenetic tree constructed from the core genome alignment file ``core_gene_alignment.aln`` [cite: 261]
* ``core_gene_alignment.vcf.gz``: contains the core genome alignment in VCF format [cite: 261]
* ``pangenome_sample.faa``: contains a sampled FASTA file of protein sequences from the pangenome, including genes from the focus reference strains [cite: 261]
* ``pangenome.emapper.annotations``: contains functional annotations for the pangenome generated by eggnog-mapper, including COG categories, GO terms, KEGG pathways, and other functional information for each gene cluster [cite: 261, 262]


..  code-block:: console

    out
    |____unitigs
    |
    |____unitigs.unique_rows.Rtab.gz [cite: 263]
    | |____unitigs.unique_rows_to_all_rows.txt [cite: 263]
    |
    |____unitigs.txt.gz [cite: 264]

* ``unitigs.unique_rows.Rtab.gz``: contains the unique unitig patterns found across the input genomes. [cite: 264]
  The number of lines represents the number of unique tests that need to be corrected for in the association analysis [cite: 265]
* ``unitigs.unique_rows_to_all_rows.txt``:  provides information on the mapping from the unique unitig patterns to all instances of those patterns observed across the input genomes [cite: 265]
* ``unitigs.txt.gz``: contains the list of unitigs counted across the input genomes and which samples encode for them [cite: 265]
