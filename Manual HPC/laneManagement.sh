#!/bin/sh

INPUT=$1
ISOLATE=${1%_L001_R1.fastq.gz}

INDIR="resources/reads/"
OUTDIR="results/00_append/"

PATH_L001_R1="${INDIR}${ISOLATE}_L001_R1.fastq.gz"
PATH_L001_R2="${INDIR}${ISOLATE}_L001_R2.fastq.gz"
PATH_L002_R1="${INDIR}${ISOLATE}_L002_R1.fastq.gz"
PATH_L002_R2="${INDIR}${ISOLATE}_L002_R2.fastq.gz"

OUT_PATH_R1="${OUTDIR}${ISOLATE}_R1"
OUT_PATH_R2="${OUTDIR}${ISOLATE}_R2"

cat << endcommand
#!/bin/sh
#SBATCH --qos bbshort
#SBATCH --ntasks 1
#SBATCH --time 5:0
#SBATCH MEM=16GB
#SBATCH OBFS=16GB

set -e

module purge; module load bluebear

cat $PATH_L002_R1 $PATH_L001_R1 > $OUT_PATH_R1 \
; \
cat $PATH_L002_R2 $PATH_L001_R2 > $OUT_PATH_R2
endcommand
