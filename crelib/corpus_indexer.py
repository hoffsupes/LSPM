
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Complete Corpus indexer
@library function created to create the p_causal baseline result  
"""
import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    import indexer
else:
    from . import indexer

indexer.parameter_config.corpus_index_name = '100_million_pure_corpus_index'
indexer.parameter_config.doctype = 'cause_effect_pairs'
copidx = indexer.parameter_config.corpus_index_name;

ID = sys.argv[1];
filepath = str(ID) + '.txt'
with open(filepath,'a+') as filew:
	indexer.index_corpus(filew,copidx)	
