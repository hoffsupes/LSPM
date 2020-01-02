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

for ((i=1; i<=8;i++)) 
do
	echo "starting process ${i}"
	time python3 get_new_old_network.py batch/ipfiles/${i}.txt batch/cleaned/${i}_cleaned.txt batch/causal/${i}_new.txt batch/cause/${i}.jsonl batch/causal/${i}_old.txt batch/cause_old/${i}.jsonl &
done

