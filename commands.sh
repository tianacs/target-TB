mykrobe predict --sample TB_48 -t 6 --skeleton_dir mykrobe_skeleton --ont --format json --min_proportion_expected_depth 0.20 --species tb -m 2048MB -T data/targets/TB_amplicons_rpoB.bed -o TB_barcode48_amplicon.mykrobe.json -i data/reads/barcode48/*
docker run --rm -it -v \\wsl$\Ubuntu\home\tianacs\sandbox\ebi_mykrobe:/mykrobe_data  mykrobe_amplicon bash
