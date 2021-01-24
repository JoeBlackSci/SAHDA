Mycogenomics Genome Assembly and Query Workflow
================================================

[![Version](https://img.shields.io/badge/Version-0.4.0-red)](https://github.com/JoeBlackSci/genome_assembly_mp1)
[![Snakemake](https://img.shields.io/badge/snakemake-5.32.0-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
[![Snakemake](https://img.shields.io/badge/Conda-4.9.2-brightgreen.svg?style=flat)](https://docs.conda.io/projects/conda/en/latest/index.html)

<img align="left" width="200" src="ZPic.png" style="padding-right: 10px">

|       **Document:**|    |
|-------------------:|:---|
| **Creation Date:** |    |
|        **Author:** | J. Blackwell, M. McDonald |
|       **License:** |    |
|       **Contact:** | j.blackwell@warwick.ac.uk |

<br>
<br>
<br>

> **Overview:** Workflow tool designed to detect and analyse genes of interest within small haplotype genomes. The workflow will compile haploid genomes, create a local database and query genes of interest. Where genes of interest are detected, a multiple alignment is performed for each target gene and a map of samples with common alleles generated.

## Method
### Inputs
+ Raw fastq reads (2 or 4 files due to lane)
+ Reference genome
+ Query gene sequences
+ Adaptor sequence

### Steps
1. Trimming \[[trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic)\]
1. ? Quality control
1. Denovo assembly \[[SPAdes](https://cab.spbu.ru/software/spades/)\]
1. Create local BLAST databases for each contigs \[[BLAST+](https://www.ncbi.nlm.nih.gov/books/NBK279690/)\]
    1. ? Write all databases to a centralised folder
1. Query each databse for sequence \[[BLAST+](https://www.ncbi.nlm.nih.gov/books/NBK279690/)\]
1. Extract sequence from the database (python script)
    1. Ensure correct orientiation
1. Perform multiple alignment for each identified gene (MAFFT for adding in more alignments?)
1. Generate a map of common alleles


## Tutorial

### Required software
> This workflow requires the installation of miniconda3 and snakemake. It is recommended that mamba is also installed.

These are the methods, as recommended by the [snakemake documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) for installing the software required for this workflow.

#### Miniconda3
Follow the [miniconda3 installation instructions](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). This will install the latest version of the [Conda](https://conda.io/en/latest/index.html) package and environment management software and it's minimal dependancies.

- Install **miniconda3** and not miniconda2 or a version of anaconda

- Answer **YES** when asked if conda should be put into and manage your **PATH**

>  The lastest version of conda should work fine but if any issues are encountered this workflow was created using conda version 4.9.2. Conda can manage it's own version.


#### Mamba
Conda is python based and can sometimes run slow or select older software versions. [mamba](https://github.com/mamba-org/mamba) is a c++ replacement for conda's package management capabilities. Install mamba using conda via the commandline.
```
conda install -c conda-forge mamba
```

#### Snakemake
[Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) is a python based workflow management language for reproducible and scalable data analysis. It is recommended to recreate the snakemake environment used to develop this workflow.

To do so, navigate using the commandline, to the top level of the workflow directory (containing this README.md file).

Recreate the snakemake environment from the config environment file.
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
<sample_name>_<total_sequences>_<R1/R2>.fastq.gz
<sample_name>_<total_sequences>_<R1/R2>.fastq
<sample_name>_<lane_no>_<R1/R2>.fastq.gz
<sample_name>_<lane_no>_<R1/R2>.fastq
```

#### Adapters
```
adaptor format
```

#### Target gene database
```
target gene databse
```

### Configuration


### Running the Workflow



## Motivation

## Documentation