Inputs
======

Phenotype file
--------------

Save your phenotype data as a tab-separated file as ``data/data.tsv``. The phenotype file should contain at least 3 columns with headers:

* ``strain``:  sample names.
* ``fasta``: relative or absolute path to the assemblies (SAMPLE.fasta).
* ``phenotype``: target phenotype(s). There can be more than one target phenotye and the column name will be used in populating the output directory.

Subsequent columns can contain other target phenotypes and/or any covariate. Additional columns are allowed and will be simply ignored. See an example phenotype data from the `test data <https://github.com/microbial-pangenomes-lab/gwas_template/tree/main/test>`__::

    strain	fasta	phenotype	covariate1	covariate2
    ECOR-01	test/small_fastas/ECOR-01.fasta	0	0.20035297602710966	1
    ECOR-02	test/small_fastas/ECOR-02.fasta	1	0.8798471273587852	1
    ECOR-03	test/small_fastas/ECOR-03.fasta	0	0.008404161045130532	0
    ECOR-04	test/small_fastas/ECOR-04.fasta	0	0.04728873355931962	1

.. note::
    Only the target variables/phenotype indicated in the ``config/config.yaml`` file will be used for the associations.
    See :doc:`usage` for more information.


Sample's genome sequences
-----------------------------------------

By default, the microGWAS pipeline takes the assemblies with the ``.fasta`` extensions.
Make sure that each sample assembly file follows this naming convention before running the analysis.

.. note::
    The pipeline now uses ggCaller to generate GFF annotations automatically, so you no longer need to provide GFF files for your samples.
