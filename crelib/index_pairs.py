
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################


"""

Index the cause effect pairs into the given index name

Various parameters described:
inpath: Path to the input cause effect pairs and evidences in jsonl format
given_index_name: Name of index to store everything to
given_doc_type: Name of doc to store everything to

@example command line usage:

python3 crelib index cause_effects.jsonl

"""

import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	import parameter_config
	from indexer import persistent_indexing
else:
	from . import parameter_config
	from .indexer import persistent_indexing

import jsonlines

"""
Indexing done with cause effect json file and causal sentence file
"""
def do_indexing_for_causes_effects(inpath,causal_sentences_path,given_index_name,given_doc_type):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	parameter_config.create_new_index(es,given_index_name);

	csens = open(causal_sentences_path,'r');

	with jsonlines.open(inpath, mode='r') as filereader:
		for ceff,causal_sent in zip(filereader,csens):
			persistent_indexing(ceff['cause'],ceff['effect'],[causal_sent.strip()],given_index_name,given_doc_type)

	csens.close()

"""
Indexing done directly using cause effects json file
"""
def do_indexing_for_causes_effects_direct(inpath,given_index_name,given_doc_type):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	print(parameter_config.create_new_index(es,given_index_name))

	with jsonlines.open(inpath, mode='r') as filereader:
		for ceff in filereader:
			persistent_indexing(ceff['cause'],ceff['effect'],ceff['evidences'],given_index_name,given_doc_type)

def do_indexing_for_causes_effects_batch(inpath,given_index_name,given_doc_type,batch_size=1000000):
	# import os
	# inputfirstname = inpath[:inpath.rfind('.jsonl')]
	# bash_command = 'sort -u ' + inpath + ' > ' + inputfirstname + '__unique.jsonl'	### Module 3a: Get unique values from them
	# os.system(bash_command)
	# newpath = inputfirstname + '_unique.jsonl';
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	from elasticsearch import helpers
	print(parameter_config.create_new_index(es,given_index_name))
	A = [];
	with jsonlines.open(inpath, mode='r') as filereader:
		for i,ceff in enumerate(filereader):
			A.append({'_op_type':'index','_type':given_doc_type,'_index':given_index_name,'_source':ceff})
			if(i%batch_size == 0):
				res = helpers.bulk(es, A)
				A = []
	if(len(A)):
		res = helpers.bulk(es, A)


"""
@Spark intermediate function: indexing for a tuple of (cause effect pair,index_name,doc_type) 
"""
def do_indexing_one(input_tuple):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	ceffdict,given_index_name,given_doc_type = input_tuple;
	parameter_config.create_new_index(es,given_index_name);
	persistent_indexing(ceffdict['cause'],ceffdict['effect'],ceffdict['evidences'],given_index_name,given_doc_type)
	return 1;

"""
@Spark intermediate function: indexing for many tuples of (cause effect pair,index_name,doc_type) 
"""
def do_indexing_many(input_tuples):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	for i,input_tuple in enumerate(input_tuples):
		ceffdict,given_index_name,given_doc_type = input_tuple;
		if(i == 0):
			parameter_config.create_new_index(es,given_index_name);
		persistent_indexing(ceffdict['cause'],ceffdict['effect'],ceffdict['evidences'],given_index_name,given_doc_type)
	return iter([1]);

"""
If you use the file directly instead of a module in a library then the main function is used
"""

def main():
	inpath = sys.argv[1];

	try:
		given_index_name = sys.argv[2];	
		given_doc_type = sys.argv[3];
	except:
		given_index_name = parameter_config.index_name;
		given_doc_type = parameter_config.doctype;
	do_indexing_for_causes_effects_batch(inpath,given_index_name,given_doc_type)

"""
If you use the file through the command line as opposed to using it as a library file
"""
if __name__ == '__main__':
	main()
