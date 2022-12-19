#!/usr/bin/env bash
set -eux

READS_DIR="/home/tianacs/sandbox/ebi_mykrobe/data/reads/barcode48"
SAMPLE="TB_48"
THREADS="6"
DEPTH="0.2"

i=0
while read -r l;
do
    echo "$l" > "./targets/target_$((++i)).bed"
    docker run --rm -v $READS_DIR:/reads -v $(pwd):/workdir mykrobe_amplicon bash -c "mykrobe predict --sample $SAMPLE -t $THREADS --skeleton_dir /workdir/mykrobe_skeleton --ont --format json --min_proportion_expected_depth $DEPTH --species tb -m 2048MB -T /workdir/targets/target_$i.bed -o /workdir/$SAMPLE.$i.mykrobe_test.json -i /reads/*.fastq.gz"
done < TB_amplicons.bed
