Mycogenomics Genome Assembly and Target Gene Multiple Alignment Workflow
================================================

[![Version](https://img.shields.io/badge/Version-1.0.0-green)](https://github.com/JoeBlackSci/genome_assembly_mp1)
[![Snakemake](https://img.shields.io/badge/snakemake-5.32.0-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
[![Conda](https://img.shields.io/badge/Conda-4.9.2-brightgreen.svg?style=flat)](https://docs.conda.io/projects/conda/en/latest/index.html)

<img align="left" width="200" src="ZPic.png" style="padding-right: 10px">

|     **Authors:**| J. Blackwell, M. McDonald |
|-------------------:|:---|
| **Creation Date:** | 12-02-2020   |
|       **License:** |    |
|       **Contact:** | j.blackwell@warwick.ac.uk |

<br>
<br>
<br>

> **Overview:** Workflow tool designed identify gen and analyse genes of interest within small haplotype genomes. The workflow will compile haploid genomes, create a local database and query genes of interest. Where genes of interest are detected, a multiple alignment is performed for each target gene and a map of samples with common alleles generated.

## Method
### Inputs
* Short-read paired end fastq files.
* Query gene fasta files.
* Adapter fasta file.

### Steps
1. Trimming \[[trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)\]
1. ? Quality control
1. Denovo assembly \[[SPAdes](https://cab.spbu.ru/software/spades/)\]
1. Create local BLAST databases for each contigs \[[BLAST+](https://www.ncbi.nlm.nih.gov/books/NBK279690/)\]
1. Query each databse for sequence \[[BLAST+](https://www.ncbi.nlm.nih.gov/books/NBK279690/)\]
1. Extract sequence from the database \[[BLASTtoGFF](https://doi.org/10.1016/j.fgb.2015.04.012)\]
1. Perform multiple alignment for each identified gene \[[MAFFT](https://mafft.cbrc.jp/alignment/software/)\]

### Outputs
* Trimmed fastq files.
* Sample denovo genome assembly.
* Local genome blast database.
* Extracted BLAST hits for query genes.
* Multiple alignment between samples for query gene.


## Tutorial

### Required software
> This workflow requires the installation of miniconda3 and snakemake. It is recommended that mamba is also installed.

These are the methods, as recommended by the [snakemake documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) for installing the software required for this workflow.

#### Miniconda3
Follow the [miniconda3 installation instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). This will install the latest version of the [Conda](https://conda.io/en/latest/index.html) package, environment management software and it's minimal dependancies.

- Install **miniconda3** and not miniconda2

- Answer **YES** when asked if conda should be put into and manage your **PATH**

>  Install the lastest version of conda, however, if any issues are encountered revert to conda version 4.9.2 used to build this workflow. Conda can manage it's own installation version.


#### Mamba
Conda is python based and can sometimes run slow or select older software versions. [mamba](https://github.com/mamba-org/mamba) is a c++ replacement for conda's package management capabilities. Install mamba using conda via the commandline.
```
conda install -c conda-forge mamba
```
> Again, install the lastest version. If issues are encountered this workflow was created using mamba v0.7.8

#### Snakemake
[Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) is a python based workflow management language for reproducible and scalable data analysis. It is recommended to recreate the snakemake environment used to develop this workflow.

To do so, navigate using the commandline, to the top level of the workflow directory (containing this README.md file).

Recreate the snakemake environment from the environment.yml `"env_snakemake_mgw.yml"` file in the config folder.
```
mamba env create -f ./config/env_snakemake_mgw.yml
```

Activate the recreated snakemake environment.
```
conda activate env_snakemake_mgw
```

> In order to return to the base conda environment input the following command. But be sure to re-activate the env_snakemake_mgw before runnnig the workflow.
> ```
> conda activate base
> ```

### Input data

#### Paired end reads
This workflow will accept paired-end short read sequences with filenames of the following formats.
```
<sample_name>_<R1/R2>.fastq.gz
<sample_name>_<lane_no>_<R1/R2>.fastq.gz
```
##### Example filenames
```
SRRXXXXXXX_R1.fastq.gz
AAAXXXX_L001_R1.fastq.gz
```

> Note: The workflow only supports samples spread over two lanes. i.e. only L001 and L002 are currently supported.

#### Adapters
The adapter file, in `.fasta` format, should be added to the `resources/adapters` file and the full filename specified in the `config/config.yml` file.

#### Target gene database
Query genes should be added as individual `.fasta` files to the `resources/query` folder with the format `<gene_query>.fasta`.

### Configuration
The workflow configuration file `config/config.yml` can be edited to specify parameters for the workflow. Including samples, query genes and trimming options.

### Running the Workflow
#### Setup
If not already done so, navigate to the top level directory (containing this README.md file) and activate the workflow's snakemake environment.
```
conda activate env_snakemake_mgw
```
Add the data required for the analysis to the appropriate resources folders.

Edit the config.yml file to specify the names of samples and query genes.

#### Executing the Workflow
To execute the default workflow run the following command.
```
snakemake --cores all --use-conda
```
> Note this will use the maximum cores available on your local machine. To specify the number of cores use `--cores N` where N is the maximum number of cores to be assigned.

Snakemake will automatically determine which jobs need to be run to generate all target files. Meaning that output files that are already present will not be regenerated.


#### Specifying Target Files
To specify a specific set of output files, follow the snakemake command with a target rule to specify what steps to perform. For example:

```
snakemake --cores all --use-conda target_trim
```

The following is the list of target rules:
```
target_trim       # Trim fastq files
target_assemble   # Assemble denovo genome
target_blastdb    # Create local blast database
target_search     # Search local database for gene query
target_retreive   # Retrieve identified hit sequences
target_align      # Align retrieved sequences
```

#### Parameters
For a full list of snakemake parameters see the [snakemake documentation](https://snakemake.readthedocs.io/en/stable/executing/cli.html).

[`--use-conda`] This workflow should always be run with with `--use-conda` flag to enable each rule to download and utilise a specific conda environment.  

[`-j --jobs --cores`] **Required** Specify the maximum number of CPU cores to use in parallel. Specify `all` to use all cores available.

[`-n --dryrun`] Dry run the `Snakefile` with `-n` prior to performing an analysis to check for potential errors.

[`-p --printshellcmds`] Print the shell commands to be executed to the terminal.

[`-r --reason`] Print snakemake's reason for executing each job.

[`-R --forcerun`] List the rules that should be re-run. Snakemake does not re-perform analysis if new files are added prior to a step that combines outputs from previous steps. For example if new data has been introduced prior to a multiple alignment.  

`--list-input-changes` gives a list of output files that are affected by the inclusion of new data. This can be used to automatically trigger a `--forceun` with the following code.

```
snakemake -cores all --forcerun $(snakemake --list-input-changes) --use-conda
```

### High Compute Cluster Execution

## Motivation
