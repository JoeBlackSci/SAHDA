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
+ Raw fastq reads (2 or 4 files due to lane).
+ Reference genome
+ Query gene sequences
+ Adaptor sequence 

### Steps 
1. Trim adaptors (trimmomatic) 
    1. adaptors
    2. low quality reads (linient trimming)
1. Quality control
1. Denovo assembly (spades)
    1. Foulder for each assembly
    1. Contigs (expect many contigs)
    1. Rename contigs file
1. Create local BLAST databases for each contigs (BLAST+)
    1. Write all databases to a centralised foulder 
1. Query each databse for sequence (BLAST+)
1. Extract sequence from the database (python script)
    1. Ensure correct orientiation 
1. Perform multiple alignment for each identified gene (MAFFT for adding in more alignments?)
1. Generate a map of common alleles 

## Motivation

## Documentation

## Tutorial

## Notes
### Sequences
adaptor - barcodes - sequence - barcode - adaptor
> should be trimmed by the machine
Some reads will slip through. This is the trimming step.

### Trimmomatic
forwards
reverse

### Spades
Check latest version - bioconda up to date. 

### local BLAST databases 
efficent for smaller databases
no need to search against larger databases
Indexed FASTA file

### Python script
find bug
re-write - into python 3





