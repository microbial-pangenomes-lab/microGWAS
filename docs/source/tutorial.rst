Beginner's guide
================

This guide will walk you through conducting a comprehensive GWAS analysis on 370 *Escherichia coli* strains using the ``microGWAS`` pipeline. [cite: 290]
In the `study by Galardini et al. (2020) <https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009065>`_ , a mouse model of sepsis was used to characterize the virulence phenotype of the strains. [cite: 291]
By using ``microGWAS`` in this tutorial, you will uncover genetic variants (unitigs, gene presence/absence, rare variants, gene cluster specific k-mers) associated with this virulence phenotype. [cite: 292]

Prerequisites
-------------

- Basic command-line knowledge [cite: 293]
- Familiarity with genomic data [cite: 293]
- A computer with at least 10 GB RAM with 8 cores with a Linux operating system like Ubuntu [cite: 293]

The whole tutorial will take at least 24 hours to complete. [cite: 293]

1. Before you begin
--------------------

i. Install Conda (if not already installed):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   If you don't have Conda installed, you can install it via Miniconda. [cite: 294]
   Miniconda is a minimal installer for Conda. [cite: 295]

   a. Download the Miniconda installer: [cite: 295]

   .. code-block:: console

      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

   b. Install Miniconda: [cite: 296]

   .. code-block:: console

      bash miniconda.sh -b -p $HOME/miniconda

   c. Initialize Conda: [cite: 297]

   .. code-block:: console

      eval "$($HOME/miniconda/bin/conda shell.bash hook)"

   d. Verify the installation: [cite: 298]

   .. code-block:: console

      conda --version

   You should see the Conda version printed to the console. [cite: 298]

ii. Install mamba (if not already installed):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After installing Conda, we recommend installing Mamba, a faster alternative to Conda for package management. [cite: 299]
Mamba is the recommended way of using Snakemake's conda integration. [cite: 300]

   a. Install mamba in your base conda environment [cite: 301]

   .. code-block:: console

      conda install -n base -c conda-forge mamba

   b. Verify the mamba installation [cite: 302]

   .. code-block:: console

      mamba --version
   
   You should see the mamba version printed to the console. [cite: 302]

iii. Installing ``microGWAS``:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We recommend obtaining ``microGWAS`` by downloading the latest release from GitHub: [cite: 303]

* Visit the `releases page <https://github.com/microbial-pangenomes-lab/microGWAS/releases>`_ on GitHub. [cite: 303]
* Download the ``microGWAS.tar.gz`` file from the latest available release. [cite: 304]
   
* Unpack the downloaded file (``tar -xvf microGWAS.tar.gz``). [cite: 304]
* Navigate to the unpacked directory (``cd microGWAS``) [cite: 305]

Additional install methods are listed in the :doc:`Usage page </usage>`. [cite: 305]

iv. Set up the ``microGWAS`` conda environment (if not present already):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Add the following channels: [cite: 306]

   .. code-block:: console

      conda config --add channels bioconda
      conda config --add channels conda-forge  

   Now, create and activate the microGWAS conda environment: [cite: 306]

   .. code-block:: console

      conda env create -f environment.yml
      conda activate microGWAS

v. Prepare your input data:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

a. Create a directory structure for your input files: [cite: 307]

   .. code-block:: console

      mkdir -p data/fastas

b. Download sample genomes in ``FASTA`` format: [cite: 308]

   .. code-block:: console
   
      wget -O data/genomes.tgz https://figshare.com/ndownloader/files/21781689
   
   Extract genome FASTA files: [cite: 308]

   .. code-block:: console

      tar -xzvf data/genomes.tgz -C data/fastas/

c. Download and modify the phenotype data: [cite: 309]

   .. code-block:: console

      wget https://raw.githubusercontent.com/mgalardini/2018_ecoli_pathogenicity/master/data/phenotypes/phenotypes.tsv -O data/data.tsv

   The phenotype file contains two reference strains, "ED1a" and "IAI39". [cite: 309]
   These strains should not be included in the phenotype file as they will cause conflicts within the pipeline. [cite: 310]
   To remove these strains from you phenotype file, do the following: [cite: 311]

   .. code-block:: console 

      sed -i '/^ED1a/d;
      /^IAI39/d' data/data.tsv [cite: 311, 312]

   The following command will update your ``data/data.tsv`` file, adding the paths for fasta files. [cite: 312]

   .. code-block:: console

      awk 'BEGIN {OFS="\t"}
      
      NR==1 {print "strain", "fasta", "phenotype"}
      
      NR>1 {print $1, "data/fastas/" $1 ".fasta", $3}' data/data.tsv > temp_file &&
      
      mv temp_file data/data.tsv [cite: 313]
      
.. note::
    To provide pre-computed GFF annotations instead of executing *de novo* assembly gene calling, add an optional ``gff`` column to the command and supply the paths (e.g. ``"data/gffs/" $1 ".gff"``). [cite: 313, 314]

d. Verify the updated phenotype file: [cite: 315]

   .. code-block:: console

      head -n 5 data/data.tsv

   You should see an output similar to the example below. [cite: 315]
   The first column lists the sample IDs, the next column is the relative path [cite: 316]
   to the assemblies in fasta format. [cite: 316]
   The last column represents the phenotype: where 1 indicates that the strain is virulent, [cite: 317]
   while 0 indicates the strain is avirulent. [cite: 317]

   .. code-block:: none

      strain  fasta   phenotype [cite: 318]
      ECOR-01 data/fastas/ECOR-01.fasta       0 [cite: 318]
      ECOR-02 data/fastas/ECOR-02.fasta       1 [cite: 318]
      ECOR-03 data/fastas/ECOR-03.fasta       0 [cite: 318]
      ECOR-04 data/fastas/ECOR-04.fasta       0 [cite: 318]

e. Clean up: [cite: 319]
   
   Remove the compressed files, you do not need them anymore: [cite: 319]

   .. code-block:: console

      rm data/genomes.tgz

f. Verify your directory structure: [cite: 320]
   
  After executing the aforementioned steps, your directory structure should look something like this: [cite: 320]

   .. code-block:: none

      data/ [cite: 320]
      ├── data.tsv [cite: 320]
      ├──fastas/ [cite: 320]
      │   ├── genome1.fasta [cite: 320]
      │   ├── genome2.fasta [cite: 320]
      │   └── ... [cite: 320]

You can confirm by doing: [cite: 320]

   .. code-block:: console

      ls data/

vi. Set up the environment and configure the pipeline: [cite: 321]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

a. Set up the eggnog-mapper database: [cite: 321]

The ``microGWAS`` pipeline requires the eggnog database for functional annotation. [cite: 321]
You have two options: [cite: 322]

i. If you have an existing eggnog database: [cite: 322]
Create a symbolic link to your actual eggnog data directory. [cite: 322]

   .. code-block:: console

      ln -s /storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/ data/eggnog-mapper [cite: 323]

Remember  to replace ``/storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/`` with the actual path on your system. [cite: 323]
ii. If you do not have the eggnog database: [cite: 324]

Simply proceed to run the ``microGWAS`` pipeline. [cite: 324]
The pipeline will automatically download and setup the required eggnog database during its execution. [cite: 325]

.. note::
    Creating a symbolic link is only necessary if you're using an existing eggNOG database. [cite: 326]
    This might be preferred as the final database size is more than 50Gb; [cite: 327]
    it therefore makes sense to [cite: 327]
    setup this database once and link it in each ``microGWAS`` analysis you are carrying out. [cite: 328]

b. Configure the pipeline: [cite: 329]

   Ensure that the  ``##### params #####`` section of the ``config/config.yaml`` file matches the print out below. [cite: 329]

   .. code-block:: yaml

      targets: [ [cite: 330]
         "phenotype", [cite: 330]
      ] [cite: 330]
      
      # MLST scheme
      mlst_scheme: ecoli [cite: 330]

      # references for association summaries and annotation
      summary_references: "--reference 536 --reference CFT073 --reference ED1a --reference IAI1 --reference IAI39 --reference K-12_substr._MG1655 --reference UMN026 --reference UTI89" [cite: 330]
      annotation_references: "--focus-strain 536 --focus-strain CFT073 --focus-strain ED1a --focus-strain IAI1 --focus-strain IAI39 --focus-strain K-12_substr._MG1655 --focus-strain UMN026 --focus-strain UTI89" [cite: 330, 331]
      enrichment_reference: "IAI39" [cite: 331]
      
      # species to be used for AMR and virulence predictions
      species_amr: "Escherichia" [cite: 331]

2. Running the ``microGWAS`` pipeline
-------------------------------------

Run the bootsrapping script. [cite: 331]

   .. code-block:: console

      bash bootstrap.sh Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 [cite: 332]

This script populates the input files used for the analysis and downloads the relevant reference genomes necessary for annotating the hits for *Escherichia coli* and analyse the variants associated to the phenotype. [cite: 332]
The syntax for this script is ``bash bootstrap.sh GENUS SPECIES MAINREFERENCE REFSEQID1,[...],REFSEQIDn``, where ``REFSEQID`` indicates the NCBI assembly ID of the various reference genomes to be used in the analysis, and ``MAINREFERENCE`` the name of the main reference genome. [cite: 333]
To run the full analysis, use the following command. [cite: 334]

   .. code-block:: console

      snakemake -p annotate_summary find_amr_vag manhattan_plots heritability enrichment_plots qq_plots tree wg_metrics --cores 24 --use-conda --conda-frontend mamba [cite: 334]

This will: [cite: 334]

- Run the GWAS analysis to identify and annotate genetic variants that are associated with the virulence phenotype (``annotate_summary``) [cite: 334]
- Generate a phylogenetic tree of all isolates and the selected references (``tree``) [cite: 334]
- Identify antimicrobial resistant and virulence associated genes (``find_amr_vag``) [cite: 334]
- Perform an enrichment analysis for the genes with the associated variants, and plot the results (``enrichment_plots``) [cite: 334]
- Compute the heritability of the phenotype, determined by the genetic variants and the lineage (``heritability``) [cite: 334, 335]
- Generate QQ-plots to diagnose the association analysis (``qq_plots``) [cite: 335]
- Generate manhattan plots on the unitigs mapped to a reference (``manhattan_plots``) [cite: 335]

The analysis will be parallelized using up to 24 cores (``--cores 24``), and the [cite: 335]
necessary tools will be installed in separated conda environments (``--use-conda --conda-frontend mamba``). [cite: 335]
The whole process will likely take more than 24 hours. [cite: 336]

.. note::
   Change the ``--cores`` argument to indicate what is the maximum number [cite: 337]
   of cores that can be used to parallelize the analysis [cite: 337]

Customizing your analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can specify which :doc:`rules` you want the pipeline to run. [cite: 337]
For example, to run the pipeline without generating a phylogenetic tree: [cite: 338]

   .. code-block:: console

      snakemake -p annotate_summary manhattan_plots heritability enrichment_plots qq_plots wg_metrics --cores 24 --use-conda --conda-frontend mamba [cite: 338]

This command runs all the same analyses as before, except for generating the phylogenetic tree and identifying AMR and virulence associated genes. [cite: 338]

3. Understanding the results
----------------------------
 
``microGWAS`` generates multiple output files and figures which can be accessed from within the ``out/`` directory. [cite: 339]
For a detailed descripition of all the outputs, refer to :doc:`outputs` section of this documentation. [cite: 340]
For the purpose of this tutorial, we will focus on key results replicated from the  `Galardini et al. (2020) study <https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1009065>`_ [cite: 341, 342]

a. Unitig-based association analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Unitigs are unique DNA sequences that serve as markers for genetic variation. [cite: 342]
``microGWAS`` uses unitigs with a minimum allele frequency (MAF) of > 1%. [cite: 343]

.. image:: ../images/manhattan.png [cite: 344]
   :alt:  Manhattan plot of the associated variants [cite: 344]
   :align: center [cite: 344]

This Manhattan plot shows unitigs associated with virulence. [cite: 344]
Peaks above the red dashed line represent genomic regions strongly associated with  the virulence phenotype. [cite: 345]
These unitigs are related to three iron-uptake systems: the high-pathogenecity island (HPI), aerobactin, and the *sitABCD* operon. [cite: 346]
For a closer look at specific genomic regions of interest related to virulence factors in *E. coli*, you can generate zoomed-in Manhattan plots. [cite: 347, 348]
The focus will be on three key areas: the high pathogencity island (HPI), the aerobactin siderophore system, and the *sitABCD* iron transport operon. [cite: 348]
To created these detailed plots, run the following command first: [cite: 349]

    .. code-block:: console
        
        python3 workflow/scripts/count_patterns.py out/associations/phenotype/unitigs_patterns.txt --threshold [cite: 349]


This command uses the number of unique unitigs' presence/absence patterns to derive an appropriate p-value threshold. [cite: 349]
You should obtain a value of ``2.16E-08``. You can then run the script to generate the manhattan plots for the three regions of interest: [cite: 350]

    .. code-block:: console

        python3 workflow/scripts/manhattan_plot.py out/associations/phenotype/mapped_all.tsv IAI39 HPI.png --threshold 2.16E-08 --zoom HPI 1.05 1.25 30 [cite: 350]
        python3 workflow/scripts/manhattan_plot.py out/associations/phenotype/mapped_all.tsv IAI39 sitABCD.png --threshold 2.16E-08 --zoom sitABCD 1.95 2.05 15 [cite: 350]
        python3 workflow/scripts/manhattan_plot.py out/associations/phenotype/mapped_all.tsv IAI39 aerobactin.png --threshold 2.16E-08 --zoom aerobactin 3.4 3.8 15 [cite: 350]

.. note::
   Run ``python3 workflow/scripts/manhattan_plot.py -h`` for an explanation of the syntax used by this script [cite: 350, 351]

.. image:: ../images/zoom.png [cite: 351]
   :alt:  A zoom-in on the associated areas of the Manhattan plot for the HPI, aerobacting and *sitABCD* operon regions. [cite: 351]
   :align: center [cite: 352]


The plot was generated for the "IAI39" reference genome, and the zoomed-in views were based on the genomic positions of the regions of interest. [cite: 352]
You can also generate volcano plots to visualise the statistical significance and magnitute of the effect for the tested genetic variants. [cite: 353]
The following code will generate a volcano plots using the ``annotate_summary.tsv`` file, which contains the summary statistics and gene annotation for the unitigs association analysis. [cite: 354]

   .. code-block:: console
        
        python3 workflow/scripts/volcano_plot.py out/associations/phenotype/annotated_summary.tsv volcano.png --threshold 2.16E-08 --genes fyuA sitA iucC [cite: 354, 355]
      

This plot represents associations using unitigs as the genetic markers. [cite: 355]

.. image:: ../images/volcano.png [cite: 356]
   :alt:  A volcano plot of the associated variants. [cite: 356]
   :align: center [cite: 357]

Each point represents a specific gene. The highlighted genes belong to the high pathogenecity island, the aerobactin, and the *sitABCD* operon. [cite: 357]
The x-axis represents the average beta value (effect size), which indicates the magnitude and direction of the association between the unitigs and the virulence phenotye. [cite: 358]
Points on the right indicate positive associations and those on the left indicate negative associations. [cite: 359]
The y-axis shows the statistical significance. [cite: 360]
The red dashed horizontal line indicates the signficance threshold computed using the ``unitigs_patterns.txt`` file. [cite: 360]
Similar plots can be created using ``annotated_gpa_summary.tsv`` or ``annotated_panfeed_summary.tsv``. [cite: 361]

b. Gene cluster-specific k-mer association analysis [cite: 361]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This analysis links specific k-mers to their source genes, using ``panfeed``. [cite: 362]

.. image:: ../images/panfeed.png [cite: 363]
   :alt:  Associations plots for gene cluster specific k-mers. [cite: 363]
   :align: center [cite: 364]


These plots represent association  for gene cluster specific k-mers for *fyuA*, *iucC*, and *sitA* genes. [cite: 364]
The y-axis represents each isolate and the x-axis the k-mer positions relative to the gene start codon for each strain. [cite: 365]
The colors correspond to the -log10 of the association p-value. [cite: 366]
The dark gray regions imply that the isolates do not encode for the k-mers, while the light gray regions represent k-mers under the association threshold. [cite: 367]

c. Functional enrichment analysis [cite: 367]
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This analysis identified overrepresented functional categories among genes with associated variants. [cite: 368]

.. image:: ../images/enrich_cog.png [cite: 369]
   :alt:  Enrichment analysis of the associated unitigs for different COG categories. [cite: 369]
   :align: center [cite: 370]

The plot shows enrichment of clusters of orthologous groups (COG) categories. [cite: 370]
The y-axis of the plot represents each COG catergory, and x-axis the number of gene hits belonging to each category. [cite: 371]
The bars are colored based on the  -log10 of the enrichment corrected p-value. [cite: 372]
Bars colored in grey do not have a significant enrichment. [cite: 373]

d. Other outputs [cite: 373]
^^^^^^^^^^^^^^^^

More information about the results of the association analysis can be found within the ``out`` directory. [cite: 374]
The content of each folder/file is reported in the :doc:`outputs` section. [cite: 375]

4. Troubleshooting [cite: 375]
-------------------

If you have persistent issues, please consult the ``Troubleshooting`` :doc:`usage` guide or seek help in the `project's issue tracker <https://github.com/microbial-pangenomes-lab/microGWAS/issues>`_. [cite: 376]
