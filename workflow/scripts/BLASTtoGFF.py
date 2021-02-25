#!/usr/bin/env python
#Python 3.8.5
#Requires biopython

############### BLASTtoGFF_50percent.py ##################

# Takes blast result of a query gene set against a reference genome and returns
# gff coords and extracted reference region for hits > 50% the length of each query sequence.

# Version 1. Megan McDonald, April 2015.
# Contact Megan McDonald, megan.mcdonald@anu.edu.au

# Version 2. Joseph C. Blackwell, January 2021.
# Updated to python 3.8.5 from 2.7.5
# Contact Megan McDonald, megan.mcdonald@anu.edu.au

############### Main ###############

# Import modules
import os
import csv
import sys
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from os.path import basename

# Defining main function
def main(inFasta=None, refFasta=None, inBlast=None, outGff=None, outFasta=None, percentCover=50):

    # Define unsepcified output gff files
    if outGff is None:
        inBase = basename(refFasta)
        noExt  = os.path.splitext(inBase)[0]
        outGff = noExt + '_output.gff'

    # Define unsepcified output fasta files
    if outFasta is None:
        inBase   = basename(refFasta)
        noExt    = os.path.splitext(inBase)[0]
        outFasta = noExt + '_output.ga'

    # Define minimum proportional cover
    # Potential python 2 vs 3 conflict
    propCover = percentCover / 100

    # Initialise denovo dictionary
    denovo = {}

    # For each contig of the denovo assembly, store id and sequence
    for seq_record in SeqIO.parse(refFasta, "fasta"):
        denovo[seq_record.id]=str(seq_record.seq)

    # Initialise reference gene dictionary
    refgene = {}

    # For each query against the denovo assembly, store query id and sequence
    for seq_record in SeqIO.parse(inFasta, "fasta"):
        refgene[seq_record.id]=str(seq_record.seq)

    # Specify the BLAST output file
    # with open(inBlast, 'r') as f:
        # reader = csv.reader(f, dialect = 'excel-tab')

    f = open(inBlast, 'rt')
    reader = csv.reader(f, dialect='excel-tab')


    # Open the output files
    # outGff integrates the isolate name species
    # outFasta integrates the name species

    # with open(outGff, 'w') as gff_file, open(outFasta, 'w') as fasta_file:
    gff_file=open(outGff, 'w')
    fasta_file=open(outFasta,'w')

    # Initalise old query
    oldquery = ''

    # ??? for row in reader? (need example/toy data; what format should come out of blast search?)
    for row in reader:
        # Set information from reader rows
        query    = row[0]
        subject  = row[2]
        alignlen = row[3]
        querylen = row[4]
        qstart   = int(row[5])
        qend     = int(row[6])
        sstart   = int(row[8])
        send     = int(row[9])

        # if the query is equal to old query: discard
        if str(oldquery) == str(query):
            continue

        # if the alignment length is smaller than X% of the query: discard
        if int(alignlen) / int(querylen) <= propCover:
            continue

        elif sstart <= send:
            gff_line   = "%s\t%s\t%d\t%d" %(subject, query, sstart, send)
            seq_denovo = "%s" %(denovo[subject][sstart:send+1])

        elif sstart >= send:
            gff_line   = "%s\t%s\t%d\t%d" %(subject, query, send, sstart)
            seq_denovo = Seq(denovo[subject][send:sstart+1])
            seq_denovo = str(seq_denovo.reverse_complement())

        isolate_name = basename(refFasta).rstrip("_assembly.fasta")

        # write to outGff
        gff_file.write(gff_line + '\n')

        # write to outFasta
        fasta_name = ">%s__%s" % (isolate_name, subject)
        fasta_file.write(fasta_name + '\n')
        fasta_file.write(seq_denovo + '\n')

        oldquery = query

    gff_file.close()
    fasta_file.close()
    f.close()


# Argument handling
# ??? what is this bit?
if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(

        # update description
        description = 'Takes blast result of a query gene set against a denovo assembled genome and returns \
        gff coords and extracted reference region for hits > 50% the length of each query sequence.')

    # Define arguments
    arg_parser.add_argument("-i", "--inFasta",      default=None, required=True, help="Path to fasta file containing query gene sequences")
    arg_parser.add_argument("-r", "--refFasta",     default=None, required=True, help="Path to fasta file containing de novo assemble genome used as blast database")
    arg_parser.add_argument("-b", "--inBlast",      default=None, required=True, help="Tab delimited blast result of query genes against reference genome")
    arg_parser.add_argument("-g", "--outGff",       default=None, help="Path to gff output file")
    arg_parser.add_argument("-o", "--outFasta",     default=None, help="Path to output fasta file")
    arg_parser.add_argument("-p", "--percentCover", default=50, type=int, help="Minimum query coverage threshold for hit to be considered, given as int between 1 and 100, default 50")

    # ??? what is this?
    if len(sys.argv) == 1:
        arg_parser.print_help()
        sys.exit(1)

    # Parse arguments
    args = arg_parser.parse_args()

    # Variable Definitions
    inFasta       = args.inFasta
    refFasta      = args.refFasta
    inBlast       = args.inBlast
    outGff        = args.outGff
    outFasta      = args.outFasta
    percentCover  = args.percentCover

    # Run main function with parsed arguments
    main(inFasta, refFasta, inBlast, outGff, outFasta, percentCover)
