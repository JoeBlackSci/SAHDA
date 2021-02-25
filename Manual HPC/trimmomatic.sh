#!/bin/sh

INPUT=$1
ISOLATE=${INPUT%_R1.fastq.gz}

INDIR="resources/reads/"
OUTDIR="results/01_trim/"

ADAPTERS="PATH_TO_ADAPTERS"
ADAPTER_OPTIONS=":2:30:10"
TRIMMOMATIC_OPTIONS="LEADING:5 TRAILING:5 SLIDINGWINDOW:4:15 MINLEN:45"

PATH_R1="${INDIR}${ISOLATE}_R1.fasta.gz"
PATH_R2="${INDIR}${ISOLATE}_R1.fasta.gz"

BASEOUT="results/01_trim/${ISOLATE}_trimmed.fastq.gz"

cat << endcommand
#!/bin/sh
#SBATCH --qos bbshort
#SBATCH --ntasks 1
#SBATCH --time 5:0
#SBATCH MEM=16GB
#SBATCH OBFS=16GB

set -e

module purge; module load bluebear
module load Trimmomatic/0.39-Java-11

java -jar trimmomatic-0.39.jar PE $PATH_R1 $PATH_R2 -baseout $BASEOUT \
LLUMINACLIP:${ADAPTERS}${ADAPTER_OPTIONS} \
$TRIMMOMATIC_OPTIONS
endcommand
