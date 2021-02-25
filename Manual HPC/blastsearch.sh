#!/bin/sh

QUERY_IN=$1
BLASTDB_IN=$2

ISOLATE=${2%_blastdb}
ISOLATE=${ISOLATE#"results/03_blastdb/"}
QUERY=${1%.fastq}

INDIR=$2
OUTDIR="results/04_search/${QUERY}/${QUERY}_${ISOLATE}_blastdb/"

OUTFMT="\"6 qseqid qlen sseqid sstart send qstart qend evalue bitscore length pident \""

cat << endcommand
#!/bin/sh
#SBATCH --qos bbshort
#SBATCH --ntasks 1
#SBATCH --time 5:0
#SBATCH MEM=16GB
#SBATCH OBFS=16GB

set -e

module purge; module load bluebear
module load BLAST+/2.10.1-gompi-2020a

blastn -db $2 -query $1 -outfmt $OUTFMT -out
endcommand
