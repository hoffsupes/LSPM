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

# python3 -c "import crelib; crelib.create_subnetwork.get_network_backup('1_billion_indexer_new_total','network_backups/300_mil.jsonl')"

# time sort -u network_backups/300_mil.jsonl > network_backups/300_mil_unique.jsonl

# python3 crelib/dedup.py network_backups/300_mil.jsonl
for ((i=1; i<=4;i++)) 
do
	echo "starting process ${i}"
	time python3 crelib/index_pairs.py network_backups/500_mil_nw/${i}.jsonl 528_mil_nu_uniq_n cause_effect_pairs &
done
