
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Extract causes effects from girju's verb list given a list of causes and effects from previous network, create new network
"""

import crelib
import jsonlines
import sys
from crelib.old_verbs import verbs,reverse_verbs

ceinpath = sys.argv[1]
csoutpath = sys.argv[2]
csoutpath2 = sys.argv[3]
ceoutpath = sys.argv[4]
newdxname = sys.argv[5]

crelib.parameter_config.verbs = verbs;
crelib.parameter_config.reverse_verbs = reverse_verbs;

print('processing ce pairs from original network ......')

with jsonlines.open(ceinpath,'r') as filer:
	with open(csoutpath,'w') as filew:
		for cdict in filer:
			filew.write(cdict['evidences'][0].strip() + '\n') 

print('sentences written')

crelib.get_causal_sentences.get_causal_sentences_lines(csoutpath,csoutpath2)

print('causal sentences obtained')

crelib.get_causes_effects.get_causes_effects_line(csoutpath2,ceoutpath)

print('cause effect pairs obtained')

crelib.index_pairs.do_indexing_for_causes_effects_batch(ceoutpath,newdxname,'cause_effect_pairs')

print('index created')