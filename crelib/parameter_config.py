
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Default parameter values and imports for various functions, some present for possible use in future versions.

index_name = 'cause_effect_testing_pipeline_dev': Default index name in elastisearch
doctype = 'cause_effect_pairs': Default doctype in elastisearch

sentence_out_path = 'commoncrawl_sentences.txt' : Default value for a separate optional internal capability to store sentences within intermediate stages
corpus_index_name_25_mil_corpus = 'rpi_dataset_headlines_only_32_million_headlines_nu': Corpus index name, used for p_causal benchmark scoring calculation
corpus_index_name = 'rpi_dataset_commoncrawl_pipeline_test'	: New corpus index name
stocator_path = 'cos://gaurav-test1.s3/'; : Stocator path, present for ease of use in future versions
causal_sentence_out_path = 'causal_sentences.txt': Default value for a separate optional internal capability to store sentences within intermediate stages
cause_effect_out_path = 'causes_and_effects.txt' : Corpus index name, used for p_causal benchmark scoring calculation

trystopper = 20; : Number of retries for most network operations
debug_mode = 1 : Debug mode outputs where-ever applicable, may be redundant

"""

import inspect
import itertools
import pdb
import time
import csv
import os
import types
import pandas as pd
import sys
import math
import numpy as np
import nltk
import gc
from nltk.tokenize import sent_tokenize
import re


index_name = 'cause_effect_testing_pipeline_dev'
doctype = 'cause_effect_pairs'

sentence_out_path = 'commoncrawl_sentences.txt';
corpus_index_name_25_mil_corpus = 'rpi_dataset_headlines_only_32_million_headlines_nu'
corpus_index_name = 'rpi_dataset_commoncrawl_pipeline_test'
stocator_path = 'cos://gaurav-test1.s3/';
causal_sentence_out_path = 'causal_sentences.txt'
cause_effect_out_path = 'causes_and_effects.txt'

trystopper = 20;
debug_mode = 1
file_writer_mode = 'w'; ## for writing results when doing causal relation extraction
# verbs = ["cause",		## Small list of verbs whose explicit persence is looked for within a corpus
# "causes",				## Old verbs
# "result in",
# "results in",
# "resulted in",
# "induce",
# "give rise",
# "gives rise",
# "gave rise",
# "given rise",
# "generate",
# "bring about",
# "brings about",
# "brought about",
# "lead to",
# "leads to",
# "led to",
# "trigger",
# "is linked to",
# "are linked to",
# "brings forth",
# "leads up to",
# "triggers off",
# "trigger off",
# "triggered off",
# "bring on",
# "brings on",
# "brought on"]

# reverse_verbs = ["stems from",
# "stemmed from",
# "brought on by",
# "caused by",
# "resulted from",
# "results from",
# "as a result of"]


#############################################################################################################################################
#############################################################################################################################################
#######- The following verbs are a superset of the old and new verbs so that new subnetworks can be created out of this larger network-######
#############################################################################################################################################
#############################################################################################################################################

verbs = ['bring about', 'kindle', 'kick up', 'brought about', 'as a consequence', 'give rise to', 'triggers', 'initiating', 'bringing', 'evokes', 'lead', 'elicit', 'gives rise', 'induces', 'bring forth', 'generates', 'generate', 'caused', 'consequently', 'is linked to', 'contribute to', 'evoke', 'set up', 'generated', 'provoke', 'provision', 'brought on', 'spark', 'originate in', 'evoking', 'commence', 'leads up to', 'lead to', 'induce', 'trigger', 'give birth to', 'perpetuate', 'entail', 'fire up', 'educing', 'in turn', 'for this reason', 'causing', 'engender', 'educe', 'actuate', 'triggered off', 'effect', 'in consequence', 'triggers off', 'set in motion', 'generating', 'unleash', 'facilitate', 'arouse', 'leads to', 'brings forth', 'results in', 'establish', 'eventuate in', 'conduce to', 'constitute', 'put forward', 'induced', 'arousing', 'instil', 'actuating', 'stimulate', 'effectuate', 'given rise', 'provide', 'triggered', 'brings on', 'led to', 'originate', 'causative', 'activating', 'indicate', 'prompt', 'trigger off', 'stimulating', 'bring on', 'kindling', 'spark off', 'consequent', 'inducing', 'cause', 'give rise', 'activate', 'call forth', 'produce', 'instigate', 'result', 'set off', 'originating', 'brings about', 'gave rise', 'inflect', 'provoking', 'effecting', 'resulted in', 'stir up', 'occasion', 'result in', 'cofound', 'consequential', 'are linked to', 'resultant', 'causes', 'facilitating'];
reverse_verbs = ['on the grounds that', 'stemmed from', 'caused by', 'resulted from', 'now that', 'stems from', 'brought on by', 'due to', 'owing to', 'as a result of', 'on account of', 'results from', 'because', 'in response to'];

#############################################################################################################################################
#############################################################################################################################################

"""
Create new index for elasticsearch
"""
def create_new_index(es,index_name):			
    try:
        ret = es.indices.create(index=index_name)#,wait_for_active_shards=all);
    except Exception as E:
        ret = str(E);
    return ret

"""
Clone pre-existing index
"""

def clone_index(es,index_name,new_index_name):
	result = es.reindex({"source": {"index": index_name},"dest": {"index": new_index_name}}, wait_for_completion=True, request_timeout=999999)
	return result;

