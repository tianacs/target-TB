#!/usr/bin/env bash
set -eux

# Specify where the reads are
READS_DIR=$2
# Specify an output directory
OUT_DIR="${3:-"./out"}"
# Give a sample name
SAMPLE=$1
THREADS="6"
DEPTH="0.2"

i=0
mkdir -p $OUT_DIR targets

while read -r l;
do
    echo "$l" > "./targets/target_$((++i)).bed"
    docker run --rm -v $READS_DIR:/reads -v $(pwd):/workdir mykrobe_amplicon bash -c "mykrobe predict --sample $SAMPLE -t $THREADS --skeleton_dir /workdir/mykrobe_skeleton --ont --format json --min_proportion_expected_depth $DEPTH --species tb -m 2048MB -T /workdir/targets/target_$i.bed -o /workdir/$OUT_DIR/$SAMPLE.$i.mykrobe.json -i /reads/*.fastq.gz"
done < TB_amplicons.bed

python merging_v2.py $SAMPLE $OUT_DIR
mv $SAMPLE.merged.output.json $OUT_DIR
#rm "TB_48".*."mykrobe.json"