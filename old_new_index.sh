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

for ((i=1; i<=4;i++)) 
do
	echo "starting process ${i}"
	time python3 crelib/index_pairs.py batch/cause/${i}.jsonl 589_mil_new cause_effect_pairs &
	time python3 crelib/index_pairs.py batch/cause_old/${i}.jsonl 589_mil_old cause_effect_pairs &
done

echo "Done!"
