#!/usr/bin/env python
#Python 2.7.5 
#Requires biopython

############### BLASTtoGFF_50percent.py ##################

# Takes blast result of a query gene set against a reference genome and returns
# gff coords and extracted reference region for hits > 50% the length of each query sequence.

#Version 1. Megan McDonald, April 2015.
#Contact Megan McDonald, megan.mcdonald@anu.edu.au

###Import modules
import os
import csv
import sys
import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from os.path import basename


def main(inFasta=None, refFasta=None, inBlast=None, outGff=None, outFasta=None, percentCover=50):

	if outGff is None:
		inBase = basename(refFasta)
		noExt = os.path.splitext(inBase)[0]
		outGff= noExt + '_output.gff'

	if outFasta is None:
		inBase = basename(refFasta)
		noExt = os.path.splitext(inBase)[0]
		outGff= noExt + '_output.fa'

	propCover = percentCover / 100

	#Initialise dictionary
	denovo={}

	for seq_record in SeqIO.parse(refFasta, "fasta"):
		denovo[seq_record.id]=str(seq_record.seq)

	refgene={}

	## This is the reference gDNA file that you used for the BLAST queries
	for seq_record in SeqIO.parse(inFasta, "fasta"):
		refgene[seq_record.id]=str(seq_record.seq)
	
	# This is an output file that integrates the isolate name species
	gff_file= open(outGff, 'w')
	
	# This is the second output file which integrates the name species
	fasta_file=open(outFasta,'w')
	
	# Need to specify where the BLAST output file is
	f = open(inBlast, 'rt')
	
	reader = csv.reader(f,dialect='excel-tab')

	oldquery=''
	
	for row in reader:
		query=row[0]
		subject=row[1]
		querylen=row[4]
		alignlen=row[3]
		qstart=int(row[5])
		qend=int(row[6])
		sstart=int(row[8])
		send=int(row[9])

		if str(oldquery)==str(query):
			continue
		
		if int(alignlen)/int(querylen)<=propCover:
			continue
		
		elif sstart<=send:
			gff_line= "%s\t%s\t%d\t%d" % (subject, query, sstart, send)
			fasta_name= ">%s__%s" % (query,subject)
			seq_denovo= "%s" %(denovo[subject][sstart:send+1])
			gff_file.write(gff_line+"\n")
			fasta_file.write(fasta_name+"\n")
			fasta_file.write(seq_denovo+"\n")
		
		elif sstart>=send:
			gff_line= "%s\t%s\t%d\t%d" % (subject, query, send, sstart)
			fasta_name= ">%s__%s" % (query,subject)
			seq_denovo= Seq(denovo[subject][send:sstart+1])
			seq_denovo=seq_denovo.reverse_complement()
			str_seq_denovo=str(seq_denovo)
			gff_file.write(gff_line+"\n")
			fasta_file.write(fasta_name+"\n")
			fasta_file.write(str_seq_denovo+"\n")
		
		oldquery=query

	gff_file.close()
	fasta_file.close()

if __name__== '__main__':
	###Argument handling.
	arg_parser = argparse.ArgumentParser(
		description='Takes blast result of a query gene set against a denovo assembled genome and returns \
		gff coords and extracted reference region for hits > 50% the length of each query sequence.')
	arg_parser.add_argument("-i","--inFasta", default=None, required=True, help="Path to fasta file containing query gene sequences")
	arg_parser.add_argument("-r","--refFasta", default=None, required=True, help="Path to fasta file containing de novo assemble genome used as blast database")
	arg_parser.add_argument("-b","--inBlast", default=None, required=True, help="Tab delimited blast result of query genes against reference genome")
	arg_parser.add_argument("-g","--outGff", default=None, help="Path to gff output file")
	arg_parser.add_argument("-o","--outFasta", default=None, help="Path to output fasta file")
	arg_parser.add_argument("-p","--percentCover", default=50, type=int, help="Minimum query coverage threshold for hit to be considered, given as int between 1 and 100, default 50")

	if len(sys.argv)==1:
		arg_parser.print_help()
		sys.exit(1)

	#Parse arguements
	args = arg_parser.parse_args()

	###Variable Definitions
	inFasta=args.inFasta
	refFasta=args.refFasta
	inBlast=args.inBlast
	outGff=args.outGff
	outFasta=args.outFasta
	percentCover=args.percentCover

	main(inFasta, refFasta, inBlast, outGff, outFasta, percentCover)