
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Create subnetwork files from an existing network.

Use only if original network created from combined set of verbs and you want to split it into two networks

@cli usage:
python3 crelib/create_subnetwork.py verb_option['new' or 'old'] new_network_index_name new_network_doc_type old_network_name filename[if network created already] mode['get_sentence' or 'create subnetwork']

"""

import sys
import jsonlines
import os

"""
Create sentence files for the subnetwork
"""
def create_sentence_files(option,network_name,network_doc,given_index_name,filename):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
		if option == 'new':
			import new_verbs as vli
		else:
			import old_verbs as vli
		from parameter_config import create_new_index
		from causal_identification import get_all_cause_effects_custom_list
		from indexer import persistent_indexing
	else:
		from .config import es
		if option == 'new':
			from . import new_verbs as vli
		else:
			from . import old_verbs as vli
		from .parameter_config import create_new_index
		from .causal_identification import get_all_cause_effects_custom_list
		from .indexer import persistent_indexing

	# print(create_new_index(es,network_name))

	verbs = vli.verbs
	reverse_verbs = vli.reverse_verbs;
	with open(filename,'a+') as filew:
		for verb in verbs+reverse_verbs:
			page = es.search(
			index = given_index_name,
			scroll = '2m',
			size = 10000,
			body = { "query": { "match_phrase":{ "evidences":verb } } })
			sid = page['_scroll_id']
			scroll_size = page['hits']['total']
			causal_sents = [r['_source']['evidences'][0] for r in page['hits']['hits']];
			[filew.write(sen.strip()+'\n') for sen in causal_sents];

		while (scroll_size > 0):
			
			page = es.scroll(scroll_id = sid, scroll = '2m')
			sid = page['_scroll_id']
			scroll_size = len(page['hits']['hits'])
			
			causal_sents = [r['_source']['evidences'][0] for r in page['hits']['hits']];
			[filew.write(sen.strip()+'\n') for sen in causal_sents];
		 
"""
Create subnetworks directly
"""
def create_subnetworks(option,network_name,network_doc,infilename):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
		if option == 'new':
			import new_verbs as vli
		else:
			import old_verbs as vli
		from parameter_config import create_new_index
		from causal_identification import get_all_cause_effects_custom_list
		from indexer import persistent_indexing
	else:
		from .config import es
		if option == 'new':
			from . import new_verbs as vli
		else:
			from . import old_verbs as vli
		from .parameter_config import create_new_index
		from .causal_identification import get_all_cause_effects_custom_list
		from .indexer import persistent_indexing
		
	verbs = vli.verbs
	reverse_verbs = vli.reverse_verbs;
	print(create_new_index(es,network_name))
	causal_sents = []
	with open(infilename,'r') as filer:
		causal_sents = filer.readlines()
	cdict = get_all_cause_effects_custom_list(causal_sents,verbs,reverse_verbs)
	keys = list(cdict.keys());
	totlen = len(keys)
	print('Elements to be indexed:',totlen)
	for i,key in enumerate(cdict.keys()):
		if(i%int(0.1*totlen) == 0):
			print((i/(1.0*totlen))*100,'% done!')
		persistent_indexing(cdict[key]['cause'],cdict[key]['effect'],cdict[key]['evidences'],network_name,network_doc); 

"""
Get all cause effect pairs within the network and write them to a file
"""
def get_all_results(given_index_name,filename):
	import sys
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	page = es.search(
	index = given_index_name,
	scroll = '2m',
	size = 10000,
	body = {'query': {'match_all':{}}})
	sid = page['_scroll_id']
	scroll_size = page['hits']['total']
	with open(filename,'a+') as filew:
		causal_sents = [r['_source']['evidences'][0] for r in page['hits']['hits']];
		[filew.write(sen+'\n') for sen in causal_sents];

		while (scroll_size > 0):
			print("Scrolling...")
			page = es.scroll(scroll_id = sid, scroll = '2m')
			sid = page['_scroll_id']
			scroll_size = len(page['hits']['hits'])
			print("scroll size: " + str(scroll_size))
			causal_sents = [r['_source']['evidences'][0] for r in page['hits']['hits']];
			[filew.write(sen+'\n') for sen in causal_sents];

def get_chunking_reduced_network(jsonfile,outjson,min_length=1):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from scoring_utils import pross_ce_phrase
	else:
		from .scoring_utils import pross_ce_phrase

	jsonfilemode = 'w';

	with jsonlines.open(jsonfile, mode='r') as filer, jsonlines.open(outjson,jsonfilemode) as filew:
		for cdict in filer:
			excause,exeffec = pross_ce_phrase(cdict['cause'],cdict['effect'])
			newcause = [c for c in excause if len(c.split(' ')) > min_length]
			neweffect = [e for e in exeffec if len(e.split(' ')) > min_length]
			if(len(newcause) == 0 or len(neweffect) == 0):
				continue;
			[filew.write({'cause':c,'effect':e,'evidences':cdict['evidences']}) for c in newcause for e in neweffect]

"""
Get all cause effect pairs within the network and write them to a jsonl file / Back up network in it's entirety
"""
def get_network_backup(given_index_name,filename):
	import sys
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	page = es.search(
	index = given_index_name,
	scroll = '2m',
	size = 10000,
	body = {'query': {'match_all':{}}})
	sid = page['_scroll_id']
	scroll_size = page['hits']['total']

	jsonfilemode = 'w'
	if(os.path.isfile(filename)):
		jsonfilemode = 'a'

	with jsonlines.open(filename, mode=jsonfilemode) as filew:
		causal_dicts = [r['_source'] for r in page['hits']['hits']];
		[filew.write(sen) for sen in causal_dicts];

		while (scroll_size > 0):
			print("Scrolling...")
			page = es.scroll(scroll_id = sid, scroll = '2m')
			sid = page['_scroll_id']
			scroll_size = len(page['hits']['hits'])
			print("scroll size: " + str(scroll_size))
			causal_dicts = [r['_source'] for r in page['hits']['hits']];
			[filew.write(sen) for sen in causal_dicts];

def main():
	opn = sys.argv[1]
	network_name = sys.argv[2]
	network_doc = sys.argv[3]
	given_index_name = sys.argv[4]
	filename = sys.argv[5]
	mode = sys.argv[6]

	if(mode == 'get_sentence'):
		create_sentence_files(opn,network_name,network_doc,given_index_name,filename)
	else:
		create_subnetworks(opn,network_name,network_doc,filename)

if __name__ == '__main__':
	main()