Usage
=====

Installation
------------

microGWAS can be obtained in three ways:

Download the latest release from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go to the `releases page on GitHub <https://github.com/microbial-pangenomes-lab/microGWAS/releases>`__
and download the ``microGWAS.tar.gz`` file from the latest available release. Then unpack it
(``tar -xvf microGWAS.tar.gz``) and move into it (``cd microGWAS``).

Clone the repository using ``git``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   git clone --recursive https://github.com/microbial-pangenomes-lab/microGWAS.git microGWAS
   cd microGWAS

You can change ``microGWAS`` to a name of your choice

Create a new repository from the GitHub template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is useful if you are planning to release your specific analysis as a reproducible
code repository, for instance by sharing your phenotype file and specific configurations
(or even edits to the existing rules). This method requires a GitHub account. Go to the
`pipeline's repository webpage <https://github.com/microbial-pangenomes-lab/microGWAS>`__
and click on the green "Use this template" button, then "Create a new repository" (or `use this link directly <https://github.com/new?template_name=microGWAS&template_owner=microbial-pangenomes-lab>`__). Once your repository is ready you can clone it locally using the
``git clone --recursive`` command.

Other preparatory steps
-----------------------

Creating the base ``microGWAS`` environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you do not have ``conda`` you can install it through
`miniconda <https://conda.io/miniconda.html>`_ and then add the necessary
channels::

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge

Then run::

    conda env create -f environment.yml
    conda activate microGWAS

Setup the ``eggnog-mapper`` database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``microGWAS`` pipeline requires the eggnog database for functional annotation. 
If you have an existing eggnog database and want to use it, create a symbolic link to your actual eggnog data directory. 

.. code-block:: console

   ln -s /fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/ data/eggnog-mapper

.. note::

    You will need to replace ``/fast-storage/miniconda3/envs/eggnog-mapper/lib/python3.9/site-packages/data/`` with the actuall path to the eggnog-mapper on your system.

If you do not have the eggnog database, proceed to run the ``microGWAS`` pipeline. The pipeline will automatically download and setup the required eggnog database during its execution.
You will not need to create a symbolic link in this case.

Configure the pipeline run
--------------------------

Prepare the input phenotype file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The microGWAS pipeline requires three inputs: the information on the target phenotype(s), and assemblies and annotations for each sample. See :doc:`inputs` for more information on the expected inputs.

Edit the pipeline configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next, edit the ``##### params #####`` section of the ``config/config.yaml`` file (at the top). These include:

* ``targets``: Name of the columns in the phenotypes file to be used in the associations. In the example below the target `phenotype` will be the one considered to test for the associations. `phenotype2` is commented (# in front) and will simply be ignored.

.. code-block::

   targets: [
            "phenotype"
            #"phenotype2",
            ]

.. note::
    Here, phenotype2 is commented (#) and will be ignored.

..  tip::

    If you have many phenotypes (>5), consider applying a more stringent cutoff post-analysis.

* ``covariates``: Covariates to be used for the associations for each phenotype. THe numbers refer to the columns in the phenotype file that should be used as covariates. The suffix "q" is added when they are quantitative and not binary. The column numering is 1-based. `See also <https://pyseer.readthedocs.io/en/master/usage.html#phenotype-and-covariates>`__ for more information. In the example below, the columns 6 and 7 are used for the target `phenotype`. The column 6 contains a quantitative covariate. The `phenotype2` is commented and will simply be ignored.

.. code-block::

    covariates:
           phenotype: "--use-covariates 6q 7"
           # phenotype2: "--use-covariates 7",

* ``MLST scheme``: Change the mlst scheme to be used to compute lineages. Find more information on the `available schemes <https://github.com/tseemann/mlst?tab=readme-ov-file#available-schemes>`__
* ``references for association summaries and annotation``: Provide the name of the references to be used for annotation of hits. Multiple strains can be provided, but only one strain can be specified to be used as a reference for the enrichment analyses. For convenience the defaults for E. coli are placed as defaults, and those for P. aeruginosa are commented.
* ``species_amr``: species to be used for AMR and virulence predictions
* ``lineages_file``: lineage file to use. By default the mlst lineages are used, but you can specify your custom lineages list.
* ``eggnogdb``: Tax ID of eggnog database to download. By default, there is the Bacteria (2). Available tax IDs can be found `here <http://eggnog5.embl.de/#/app/downloads>`__
* Filters to remove spurious hits: change them to be more or less stringent
    * ``length``:  Minimum unitig length (ignored if ``--panfeed`` is used)
    * ``min_hits``: Minimum number of strains
    * ``max_genes``: Maximum number of genes to which a unitig/kmer can map

.. note::
    For convenience the params for *E. coli* are placed as defaults, and those for *P. aeruginosa* are commented.

Which lineage file to use?
""""""""""""""""""""""""""

If you prefer to use your own lineage definitions, and not those provided by ``mlst`` (e.g. 
if you prefer poppunk), you can specify a lineage file to be used, editing the ``lineages_file`` entry.

Run the pipeline
----------------

First step is to activate the ``microGWAS`` environment. For this, run::
   
   conda activate microGWAS

Run the bootstrapping script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then run the bootstrapping script to populate the input files for the pipeline and download the reference genomes used for annotation of hits and the rare variants analyses. 
The bootstrap.sh script takes multiple arguments:

* ``Genus``: Genus of the species under study (e.g. Escherichia)
* ``Species``: Species of the species under study (e.g. coli)
* ``Reference``: Strain name for the reference to be used for rare variants (e.g. IAI39, name should be the one NCBI uses)
* ``Assemblies``: Comma separated list of NCBI assembly IDs to be downloaded as references (e.g. GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1)

The following example works for *E. coli* (and downloads the references listed by default in ``config/config.yaml``)::

   bash bootstrap.sh Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1 

The following example works for *P. aeruginosa* and matches the references listed in the ``config/config.yaml`` file::

   bash bootstrap.sh Pseudomonas aeruginosa UCBPP-PA14 GCF_000006765.1,GCF_000014625.1 

It is also possible to provide a number of local "private" assemblies, to be used instead of those downloaded from NCBI, or alongside them.
Each local reference should have its own directory, each containing the following files:

* ``genome.fasta``: the assembly nucleotide sequence(s) in fasta format
* ``genome.gff``: the annotated assembly in gff format
* ``genome.gbk``: the annotated assembly in genbank format
* ``genome.faa``: the assembly protein sequences in fasta format (this file is optional)

To include these local assemblies alongside the ones to be downloaded from NCBI, you can use the following command::

   bash bootstrap.sh --local-dirs local/ref1,local/ref2 Escherichia coli IAI39 GCF_000013305.1,GCF_000007445.1,GCF_000026305.1,GCF_000026265.1,GCF_000026345.1,GCF_000005845.2,GCF_000026325.1,GCF_000013265.1

in which ``local/ref1`` and ``local/ref2`` are the directories containing the local assemblies. The ID of the local assemblies will be the name of the directory, so in this case ``ref1`` and ``ref2``.

In case you want to use the local assemblies only, you can omit the final positional argument::

   bash bootstrap.sh --local-dirs local/ref1,local/ref2 Escherichia coli ref1

Run the actual snakemake pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You are now ready to run the full pipeline! The following example runs all the analyses using 24 cores::

   snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots tree wg_metrics --cores 24 --verbose --use-conda

Running specific rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pipeline also allows for executing specific rules.
To run the pipeline up to the pangenome analysis::

   snakemake -p pangenome --cores 24 --use-conda --cores 24 --verbose --use-conda

The following example instead uses "vanilla" ``conda`` and skips the generation of the phylogenetic tree::
   

   snakemake -p annotate_summary find_amr_vag map_back manhattan_plots heritability enrichment_plots qq_plots --cores 24 --verbose --use-conda

See :doc:`rules` for more information on what each rule does.

Troubleshooting
---------------

For issues with installing or running the software please raise an `issue on github <https://github.com/microbial-pangenomes-lab/microGWAS/issues>`__

Avoid using samples as references
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using a strain with an identifier both in the dataset and as a reference can cause various errors (e.g. with the ``map_back`` rule) in the pipeline.
Please make sure sample and reference identifiers do not overlap.

Testing
-------

We have included a small dataset in order to test the pipeline installation in reasonable time and resources. In its current state continuous integration (CI) in the cloud is not feasible because certain rules require significant time and resources to complete (``annotate_reference``, ``get_snps``). Some workarounds might be added in the future to bypass those rules. 
In the meantime the tests can be run on a decent laptop with 8 cores and at least ~10Gb RAM in a few hours. The test dataset has been created from that `used in a mouse model of bloodstream infection <https://github.com/microbial-pangenomes-lab/microGWAS/blob/main>`__

To run the tests, prepare a symbolic link to the eggnog-mapper databases (as explained above), then do the following::

   cd test
   bash run_tests.sh

The script will prepare the input files, run the bootstrapping script, then run snakemake twice,
first in "dry" mode, and then "for real". Please note that the only rule that is not tested
is the one estimating lineages (``lineage_st``), as the test dataset is a
reduced part of the *E. coli* genome,
and therefore it would report each isolate with an unknown ST.
