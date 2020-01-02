
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    import indexer
else:
    from . import indexer

## index name
indexer.parameter_config.index_name = '100_million_index_creator_new_index_corpus_new_1_copy_2'
#indexer.parameter_config.index_name = 'askljnlasn_91811kkakA'
## doctype
indexer.parameter_config.doctype = 'cause_effect_pairs'

## filepath obtained from the commandline
ID = sys.argv[1];
filepath = str(ID)# + '.txt'
#filepath = '/home/garoov/Downloads/complete.txt'

## direct function for network creation
indexer.run_data_single(filepath,1)
