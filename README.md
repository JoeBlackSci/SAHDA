Mycogenomics Genome Assembly and Query Workflow
================================================
> **Overview:** Workflow tool designed to detect and analyse genes of interest within small haplotype genomes. The workflow will compile haploid genomes, create a local database and query genes of interest. Where genes of interest are detected, a multiple alignment is performed for each target gene and a map of samples with common alleles generated. 

## Specification
- Input directory
- Specified conda enviroments
- Automated or semi-automated
- What form of user interaction?
    - command line
    - command file 
- What form of documentation? 
- What form of setup?
    - Done through github or through make file?
    - Just add data


## Method
### Inputs
+ Genome sequences
+ Reference genome
+ Query gene sequences

### Steps 
1. Trim adaptors 
1. Quality control
1. Align to reference genome
    1. Convert to binary 
    1. Sort
    1. Align
1. Create local BLAST database
1. Query each genome for genes
1. Perform multiple alignment for each identified gene (MAFFT for adding in more alignments?)
1. Generate a map of common alleles 

## Motivation
