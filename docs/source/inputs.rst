Inputs
=====

Phenotype file
------------

Save your phenotype data as a tab-separated file as ``data/data.tsv``. The phenotype file should contain at least 4 columns with headers:

* ``strain``:  sample names.
* ``fasta``: relative or absolute path to the assemblies (SAMPLE.fasta).
* ``gff``: relative or absolute path to the annotations (SAMPLE.gff).
* ``phenotype``: target phenotype.

Subsequent columns can contain other target phenotypes. Additional columns are allowed and will be simply ignored. See an example phenotype data from the `test data <https://github.com/microbial-pangenomes-lab/gwas_template/tree/main/test>`__::

    strain	fasta	gff	killed	phenotype	covariate1	covariate2
    ECOR-01	test/small_fastas/ECOR-01.fasta	test/small_gffs/ECOR-01.gff	0	0	0.20035297602710966	1
    ECOR-02	test/small_fastas/ECOR-02.fasta	test/small_gffs/ECOR-02.gff	10	1	0.8798471273587852	1
    ECOR-03	test/small_fastas/ECOR-03.fasta	test/small_gffs/ECOR-03.gff	0	0	0.008404161045130532	0
    ECOR-04	test/small_fastas/ECOR-04.fasta	test/small_gffs/ECOR-04.gff	0	0	0.04728873355931962	1

.. note::
    Only the target variables/phenotype indicated in the ``config/config.yaml`` file will be used for the associations.
    See :doc:`usage` for more information.


Sample's genome sequences and annotations
-----------------------------------------

By default, the microGWAS pipeline takes the assemblies and annotations with the ``.fasta`` and ``.gff`` extensions.
Make sure you have the right format before running the analysis.