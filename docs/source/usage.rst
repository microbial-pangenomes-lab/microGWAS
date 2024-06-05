Usage
=====

Installation
------------

microGWAS can be obtained in three ways:

Download the latest release from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**to be implemented**

Clone the repository using ``git``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

   git clone --recursive https://github.com/microbial-pangenomes-lab/gwas_template.git microGWAS
   cd microGWAS

You can change ``microGWAS`` to a name of your choice

Create a new repository from the GitHub template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is useful if you are planning to release your specific analysis as a reproducible
code repository, for instance by sharing your phenotype file and specific configurations
(or even edits to the existing rules). This method requires a GitHub account. Go to the
`pipeline's repository webpage <https://github.com/microbial-pangenomes-lab/gwas_template>`__
and click on the green "Use this template" button, then "Create a new repository" (or `use this link directly <https://github.com/new?template_name=gwas_template&template_owner=microbial-pangenomes-lab>`__). Once your repository is ready you can clone it locally using the `git clone --recursive` command.

Other preparatory steps
-----------------------

Creating the base ``microGWAS`` environment
~~~~~~~~~~~~~~~~~~~~~~

**Here explain how to install the microGWAS conda environment**

Create a symbolic link to the ``eggnog-mapper`` database
~~~~~~~~~~~~~~~~~~~~~~~~~

**Here explain how to create the symbolic link, optionally how to download the eggnog database**

Configure the pipeline run
--------------------------

Prepare the input phenotype file
~~~~~~~~~~~~~~~~~~~

**Here be very brief and link to the "inputs" page**

Edit the pipeline configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Here explain which entries can be edited and what they mean. Provide examples for E. coli and Pseudomonas**

Run the pipeline
----------------

**First step is to activate the ``microGWAS`` environment**

Run the bootstrapping script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Provide examples for E. coli and Pseudomonas, and explain the relationship between the references and the assembly codes provided to the script**

Run the actual snakemake pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Provide a couple of example snakemake commands, as in the current README, refer to the "rules" page for a breakdown of what each rule does**

Troubleshooting
------------

**Here a few known and common failure modes could be listed, together with solutions.
If we cannot think of any we can drop this section for now, or just link the issues page
on github**
