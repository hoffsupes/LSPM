
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Creates two versions of a network at once
"""

import crelib
import jsonlines
import sys
from crelib.old_verbs import verbs,reverse_verbs

inpath = sys.argv[1]
csoutpath = sys.argv[2]
csoutpath2 = sys.argv[3]
ceoutpath = sys.argv[4]
csoutpathold = sys.argv[5]
ceoutpathold = sys.argv[6]

print('ingesting data ......')

crelib.ingest_corpus.ingest_corpus(inpath,csoutpath)

print('sentences written')

crelib.get_causal_sentences.get_causal_sentences_lines(csoutpath,csoutpath2)

print('causal sentences obtained')

crelib.get_causes_effects.get_causes_effects_line(csoutpath2,ceoutpath)

print('cause effect pairs obtained')


crelib.parameter_config.verbs = verbs;
crelib.parameter_config.reverse_verbs = reverse_verbs;


crelib.get_causal_sentences.get_causal_sentences_lines(csoutpath2,csoutpathold)

print('old causal sentences obtained')

crelib.get_causes_effects.get_causes_effects_line(csoutpathold,ceoutpathold)

print('old cause effect pairs obtained')
