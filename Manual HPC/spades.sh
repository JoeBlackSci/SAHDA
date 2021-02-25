#!/bin/sh

INPUT=$1
ISOLATE=${1%_trimmed_1P.fastq}

INDIR="results/01_trim/"
OUTDIR="results/02_assemble/${ISOLATE}_assembled/"

PATH_1P="${INDIR}${ISOLATE}_trimmed_1P.fastq"
PATH_1U="${INDIR}${ISOLATE}_trimmed_1U.fastq"
PATH_2P="${INDIR}${ISOLATE}_trimmed_2P.fastq"
PATH_2U="${INDIR}${ISOLATE}_trimmed_2U.fastq"

cat << endcommand
#!/bin/sh
#SBATCH --qos bbshort
#SBATCH --ntasks 1
#SBATCH --time 5:0
#SBATCH MEM=16GB
#SBATCH OBFS=16GB

set -e

module purge; module load bluebear
module load SPAdes/3.14.1-GCC-8.3.0-Python-3.7.4

spades.py --pe1-1 $PATH_1P --pe1-2 PATH_2P --pe1-s PATH_1U --pe1-s PATH_2U -o $OUTDIR
endcommand
