#!/bin/bash
#
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################
#

for ((i=1; i<=7;i++)) 
do
    echo "started process" $i &
    python3 crelib/standalone_single_threaded_version.py batch/ipfiles/${i}.txt batch/cleaned/${i}_cleaned.txt batch/causal/${i}_causal.txt batch/cause/${i}_cause.jsonl benchmarks 1_billion_indexer_new_total cause_effect_pairs w &
done

