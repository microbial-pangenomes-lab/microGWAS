Usage
=====

Installation
------------

microGWAS can be obtained in three ways: [cite: 377]

Download the latest release from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go to the `releases page on GitHub <https://github.com/microbial-pangenomes-lab/microGWAS/releases>`__ [cite: 377]
and download the ``microGWAS.tar.gz`` file from the latest available release. [cite: 377]
Then unpack it (``tar -xvf microGWAS.tar.gz``) and move into it (``cd microGWAS``). [cite: 377, 378]

Clone the repository using ``git`` [cite: 378]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   git clone --recursive https://github.com/microbial-pangenomes-lab/microGWAS.git microGWAS
   cd microGWAS

You can change ``microGWAS`` to a name of your choice [cite: 378, 379]

Create a new repository from the GitHub template [cite: 379]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is useful if you are planning to release your specific analysis as a reproducible
code repository, for instance by sharing your phenotype file and specific configurations
(or even edits to the existing rules). [cite: 379]
This method requires a GitHub account. Go to the `pipeline's repository webpage <https://github.com/microbial-pangenomes-lab/microGWAS>`__ and click on the green "Use this template" button, then "Create a new repository" (or `use this link directly <https://github.com/new?template_name=microGWAS&template_owner=microbial-pangenomes-lab>`__). [cite: 379, 380]
Once your repository is ready you can clone it locally using the ``git clone --recursive`` command. [cite: 380, 381]

Other preparatory steps [cite: 381]
-----------------------

Creating the base ``microGWAS`` environment [cite: 381]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you do not have ``conda`` you can install it through `miniconda <https://conda.io/miniconda.html>`_ and then add the necessary channels:: [cite: 381, 382]

    conda config --add channels bioconda
    conda config --add channels conda-forge

Then run:: [cite: 382]

    conda env create -f environment.yml
    conda activate microGWAS

Setup the ``eggnog-mapper`` database [cite: 382]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``microGWAS`` pipeline requires the eggnog database for functional annotation. [cite: 382]
If you have an existing eggnog database and want to use it, create a symbolic link to your actual eggnog data directory. [cite: 383]

.. code-block:: console

   ln -s /fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/ data/eggnog-mapper [cite: 384]

.. note::

    You will need to replace ``/fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/`` with the actuall path to the eggnog-mapper on your system. [cite: 384]
If you do not have the eggnog database, proceed to run the ``microGWAS`` pipeline. [cite: 385]
The pipeline will automatically download and setup the required eggnog database during its execution. [cite: 386]
You will not need to create a symbolic link in this case. [cite: 387]

Configure the pipeline run [cite: 387]
--------------------------

Prepare the input phenotype file [cite: 387]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The microGWAS pipeline requires two inputs: the information on the target phenotype(s), and assemblies for each sample. [cite: 388]
By default, the pipeline uses ggCaller to generate GFF annotations automatically. [cite: 389]
Alternatively, a pre-computed ``gff`` column listing paths to custom GFF files can be supplied to skip de novo gene calling entirely. [cite: 390]
See :doc:`inputs` for more information on the expected inputs. [cite: 391]

Edit the pipeline configuration file [cite: 391]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, edit the ``##### params #####`` section of the ``config/config.yaml`` file (at the top). [cite: 391]
These include: [cite: 392]

* ``targets``: Name of the columns in the phenotypes file to be used in the associations. [cite: 392]
  In the example below the target `phenotype` will be the one considered to test for the associations. [cite: 393]
  `phenotype2` is commented (# in front) and will simply be ignored. [cite: 394]

  .. code-block::

     targets: [
              "phenotype"
              #"phenotype2",
              ] [cite: 395]

.. note::
    Here, phenotype2 is commented (#) and will be ignored. [cite: 395]

..  tip::

    If you have many phenotypes (>5), consider applying a more stringent cutoff post-analysis. [cite: 396]
* ``covariates``: Covariates to be used for the associations for each phenotype. [cite: 397]
  The numbers refer to the columns in the phenotype file that should be used as covariates. [cite: 398]
  The suffix "q" is added when they are quantitative and not binary. The column numbering is 1-based. [cite: 399]
  `See also <https://pyseer.readthedocs.io/en/master/usage.html#phenotype-and-covariates>`__ for more information. In the example below, the columns 6 and 7 are used for the target `phenotype`. [cite: 400]
  The column 6 contains a quantitative covariate. The `phenotype2` is commented and will simply be ignored. [cite: 401]

  .. code-block::

      covariates:
             phenotype: "--use-covariates 6q 7"
             # phenotype2: "--use-covariates 7", [cite: 402]

* ``MLST scheme``: Change the MLST scheme to be used to compute lineages. [cite: 402]
  Check the :download:`mlst scheme example file <species_samples/mlst_samples.csv>` for the correct format. See also `avaiable MLST schemes <https://github.com/tseemann/mlst?tab=readme-ov-file#available-schemes>`__ for more informations. [cite: 403]
* ``references for association summaries and annotation``: Provide the name of the references to be used for annotation of hits. [cite: 404]
  Multiple strains can be provided, but only one strain can be specified to be used as a reference for the enrichment analyses. [cite: 405]
  For convenience the defaults for E. coli are placed as defaults, and those for P. aeruginosa are commented. [cite: 406]
  The names to be indicated here should be the same as those in the reference assemblies provided with the bootstrap script (see below). [cite: 407]
* ``species_amr``: Specify the species for AMR analysis. Check the :download:`species_amr example file <species_samples/amr_samples.csv>` for the correct format. [cite: 408]
  See also `avaiable AMR schemes <https://github.com/MDU-PHL/abritamr>`__ for more informations. [cite: 409]
* ``lineages_file``: lineage file to use. [cite: 409]
  By default the mlst lineages are used, but you can specify your custom lineages list. [cite: 410]
* ``eggnogdb``: Tax ID of eggnog database to download. By default, there is the Bacteria (2). [cite: 411]
  Available tax IDs can be found `here <http://eggnog5.embl.de/#/app/downloads>`__ [cite: 412]
* Filters to remove spurious hits: change them to be more or less stringent
    * ``length``:  Minimum unitig length (ignored if ``--panfeed`` is used)
    * ``min_hits``: Minimum number of strains
    * ``max_genes``: Maximum number of genes to which a unitig/kmer can map

.. note::
    For convenience the params for *E. coli* are placed as defaults, and those for *P. aeruginosa* are commented. [cite: 412, 413]

Which lineage file to use?
""""""""""""""""""""""""""

If you prefer to use your own lineage definitions, and not those provided by ``mlst`` (e.g. if you prefer poppunk), you can specify a lineage file to be used, editing the ``lineages_file`` entry. [cite: 414]

Run the pipeline [cite: 414]
----------------

First step is to activate the ``microGWAS`` environment. [cite: 415]
For this, run:: [cite: 415]
   
   conda activate microGWAS [cite: 416]

Run the bootstrapping script [cite: 416]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then run the bootstrapping script to populate the input files for the pipeline and download the reference genomes used for annotation of hits and the rare variants analyses. [cite: 416]
The bootstrap.sh script takes multiple arguments: [cite: 417]

* ``Genus``: Genus of the species under study (e.g. Escherichia) [cite: 417]
* ``Species``: Species of the species under study (e.g. coli) [cite: 417]
* ``Reference``: Strain name for the reference to be used for rare variants (e.g. IAI39, name should be the one NCBI uses, see below) [cite: 417]
* ``Assemblies``: Comma separated list of NCBI assembly IDs to be downloaded as references (e.g. GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1) [cite: 417]

The following example works for *E. coli* (and downloads the references listed by default in ``config/config.yaml``):: [cite: 417, 418]

   bash bootstrap.sh Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 [cite: 418]

The following example works for *P. aeruginosa* and matches the references listed in the ``config/config.yaml`` file:: [cite: 418, 419]

   bash bootstrap.sh Pseudomonas aeruginosa UCBPP-PA14 GCF_000006765.1,GCF_000014625.1 [cite: 419]

We provide a list of RefSeq accessions and the corresponding names that can be used as reference for a large number of species :download:`Ref_IDS <species_samples/Ref_Genomes_Samples.csv>`. [cite: 419]

.. tip::
    If the organism you are looking for is not listed or you want to use other RefSeq entries as reference genomes, you need to know the strain name associated to your accession of choice. [cite: 419, 420]
    You can find it by searching for the assembly accession on the NCBI website, and looking for the "Strain" field in assembly page. [cite: 421]
    For example, for the accession ``GCF_000013305.1``, the corresponding strain name is ``536`` (see `here <https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000013305.1/>`__). [cite: 422]
    It is also possible to provide a number of local "private" assemblies, to be used instead of those downloaded from NCBI, or alongside them. [cite: 423]
    Each local reference should have its own directory, each containing the following files: [cite: 424]

    * ``genome.fasta``: the assembly nucleotide sequence(s) in fasta format [cite: 424]
    * ``genome.gff``: the annotated assembly in gff format (required for reference genomes only) [cite: 424]
    * ``genome.gbk``: the annotated assembly in genbank format [cite: 424]
    * ``genome.faa``: the assembly protein sequences in fasta format (this file is optional) [cite: 424]

.. note::
    For sample genomes, you only need to provide FASTA files. [cite: 424]
    The pipeline uses ggCaller to generate GFF annotations automatically for all samples unless pre-computed GFF files are specified via the optional column sheet. [cite: 425]

To include these local assemblies alongside the ones to be downloaded from NCBI, you can use the following command:: [cite: 426]

   bash bootstrap.sh --local-dirs local/ref1,local/ref2 Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 [cite: 426]

in which ``local/ref1`` and ``local/ref2`` are the directories containing the local assemblies. [cite: 426]
The ID of the local assemblies will be the name of the directory, so in this case ``ref1`` and ``ref2``. [cite: 427]
In case you want to use the local assemblies only, you can omit the final positional argument:: [cite: 428]

   bash bootstrap.sh --local-dirs local/ref1,local/ref2 Escherichia coli ref1 [cite: 428]

Run the actual snakemake pipeline [cite: 428]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You are now ready to run the full pipeline! [cite: 428]
The following example runs all the analyses using 24 cores:: [cite: 429]

   snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree wg_metrics --cores 24 --use-conda [cite: 429]

Running specific rules [cite: 429]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pipeline also allows for executing specific rules. [cite: 429]
To run the pipeline up to the pangenome analysis:: [cite: 430]

   snakemake -p pangenome --cores 24 --use-conda [cite: 430]

The following example instead uses "vanilla" ``conda`` and skips the generation of the phylogenetic tree:: [cite: 430]
   

   snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots --cores 24 --use-conda [cite: 430]

See :doc:`rules` for more information on what each rule does. [cite: 430]

Troubleshooting [cite: 431]
---------------

For issues with installing or running the software please raise an `issue on github <https://github.com/microbial-pangenomes-lab/microGWAS/issues>`__ [cite: 431]

Avoid using samples as references [cite: 431]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using a strain with an identifier both in the dataset and as a reference can cause various errors (e.g. with the ``map_back`` rule) in the pipeline. [cite: 431]
Please make sure sample and reference identifiers do not overlap. [cite: 432]

Testing [cite: 433]
-------

We have included a small dataset in order to test the pipeline installation in reasonable time and resources. [cite: 433]
In its current state continuous integration (CI) in the cloud is not feasible because certain rules require significant time and resources to complete (``annotate_reference``, ``get_snps``). [cite: 434]
Some workarounds might be added in the future to bypass those rules. [cite: 435]
In the meantime the tests can be run on a decent laptop with 8 cores and at least ~10Gb RAM in a few hours. [cite: 436]
The test dataset has been created from that `used in a mouse model of bloodstream infection <https://github.com/microbial-pangenomes-lab/microGWAS/blob/main>`__ [cite: 437]

To run the tests, prepare a symbolic link to the eggnog-mapper databases (as explained above), then do the following:: [cite: 437]

   cd test
   bash run_tests.sh [cite: 437]

The script will prepare the input files, run the bootstrapping script, then run snakemake twice, first in "dry" mode, and then "for real". [cite: 437]
Please note that the only rule that is not tested is the one estimating lineages (``lineage_st``), as the test dataset is a reduced part of the *E. coli* genome, and therefore it would report each isolate with an unknown ST. [cite: 438, 439]
