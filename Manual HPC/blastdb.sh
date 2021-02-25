#!/bin/sh

INPUT=$1
ISOLATE=${1%_assembled/contigs.fasta}
ISOLATE=${ISOLATE#"results/02_assemble/"}

INDIR=$1
OUTDIR="results/03_blastdb/${ISOLATE}_blastdb/"

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

makeblastdb -in $INDIR -dbtype nucl -out $OUTDIR
endcommand
