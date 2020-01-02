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
	time python3 create_old_network.py network_backups/500_mil_nw/${i}.jsonl network_backups/500_mil_nw/ori_verb/${i}.txt network_backups/500_mil_nw/ori_verb/${i}_causal.txt network_backups/500_mil_nw/ori_verb/${i}_cause.jsonl 528_mil_oldverbs &
done

