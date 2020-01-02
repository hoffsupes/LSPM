
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################


"""

The end to end pipeline going from sentences (present line by line within a text file) to a network (of cause effect pairs) created from 
them which are then used for scoring on a benchmark and also individually performing the binary causal question answering.

Various parameters described: 
commoncrawl_sents_path: Path to the input text corpus file (.txt file)
cleaned_commoncrawl_sents_path: Output path to cleaned corpus text file (.txt file)
causal_sents_path: Output path to file which contains all the causal sentences from the previous file (.txt file)
cause_effects_path: Output path to file which contains all the cause effect pairs from the previous file (.jsonl file)
benchmark_path: Path to the folder where the benchmark files are contained
given_index_name: Index name for elastisearch index
given_doc_type: Doc type for elastisearch index

@example command line usage:

python3 crelib/standalone_single_threaded_version.py input_test_data.txt cleaned_pipeline_test_file.txt causal_pipeline.txt cause_effects_pipeline.jsonl benchmarks

OR

python3 crelib pipeline input_test_data.txt cleaned_pipeline_test_file.txt causal_pipeline.txt cause_effects_pipeline.jsonl benchmarks

"""

import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	import parameter_config
	from get_causal_sentences import get_causal_sentences_lines
	from get_causes_effects import get_causes_effects_line
	from index_pairs import do_indexing_for_causes_effects_batch
	from benchmark_scorer import benchmark_scoring
	from binary_causal_question_answering import bcqa
	from ingest_corpus import ingest_corpus
else:
	from . import parameter_config
	from .get_causal_sentences import get_causal_sentences_lines
	from .get_causes_effects import get_causes_effects_line
	from .index_pairs import do_indexing_for_causes_effects_batch
	from .benchmark_scorer import benchmark_scoring
	from .binary_causal_question_answering import bcqa
	from .ingest_corpus import ingest_corpus

"""
@function for the complete pipeline with all the modules combined
"""
def single_threaded_standaldone_end_to_end_pipeline_time_it(commoncrawl_sents_path,cleaned_commoncrawl_sents_path,causal_sents_path,cause_effects_path,given_index_name,given_doc_type,benchmark_path):
	import time
	if(cause_effects_path.rfind('.jsonl') == -1):
		print('Cause effect output file needs to be in .jsonl format! Exiting!')
		exit()
	t1 = time.time()
	ingest_corpus(commoncrawl_sents_path,cleaned_commoncrawl_sents_path)			### Module 1: Take sentences as input
	t2 = time.time()
	print('time to ingest corpus ',t2-t1,' seconds')
	
	t3 = time.time()
	get_causal_sentences_lines(cleaned_commoncrawl_sents_path,causal_sents_path);	### Module 2: Get causal sentences from them
	t4 = time.time()
	print('time to causal sentence ',t4-t3,' seconds')
	
	t5 = time.time()
	get_causes_effects_line(causal_sents_path,cause_effects_path)					### Module 3: Get causes and effects
	t6 = time.time()
	print('time to cause effect extraction ',t6-t5,' seconds')
	
	t7 = time.time()
	do_indexing_for_causes_effects_batch(cause_effects_path,given_index_name,given_doc_type)	### Module 4: Index them
	t8 = time.time()
	print('time to cause effect extraction ',t8-t7,' seconds')
	
	print('total time taken ',t8 - t1,' seconds')
	#benchmark_scoring(given_index_name,benchmark_path)		### Module 5: Benchmark scoring

	#response = input("\nDo you want to perform binary causal question answering? (respond with 'yes' or 'y' without the quotes) :").strip(' ').strip()

	#if(response.lower() == 'yes' or response.lower() == 'y'):
		#bcqa(given_index_name)								### Optional Module: Binary Causal Question Answering

def single_threaded_standaldone_end_to_end_pipeline(commoncrawl_sents_path,cleaned_commoncrawl_sents_path,causal_sents_path,cause_effects_path,given_index_name,given_doc_type,benchmark_path):
	import os
	if(cause_effects_path.rfind('.jsonl') == -1):
		print('Cause effect output file needs to be in .jsonl format! Exiting!')
		exit()
	ingest_corpus(commoncrawl_sents_path,cleaned_commoncrawl_sents_path)			### Module 1: Take sentences as input
	get_causal_sentences_lines(cleaned_commoncrawl_sents_path,causal_sents_path);	### Module 2: Get causal sentences from them
	get_causes_effects_line(causal_sents_path,cause_effects_path)					### Module 3: Get causes and effects
	do_indexing_for_causes_effects_batch(newcause_effects_path,given_index_name,given_doc_type)	### Module 4: Index them
	benchmark_scoring(given_index_name,benchmark_path)		### Module 5: Benchmark scoring

	response = input("\nDo you want to perform binary causal question answering? (respond with 'yes' or 'y' without the quotes) :").strip(' ').strip()

	if(response.lower() == 'yes' or response.lower() == 'y'):
		bcqa(given_index_name)								### Optional Module: Binary Causal Question Answering

def single_threaded_standaldone_end_to_end_pipeline_batch(commoncrawl_sents_path,cleaned_commoncrawl_sents_path,causal_sents_path,cause_effects_path,given_index_name,given_doc_type,benchmark_path):	### remove duplicates from batch files first
	import os
	if(cause_effects_path.rfind('.jsonl') == -1):
		print('Cause effect output file needs to be in .jsonl format! Exiting!')
		exit()
	ingest_corpus(commoncrawl_sents_path,cleaned_commoncrawl_sents_path)			### Module 1: Take sentences as input
	get_causal_sentences_lines(cleaned_commoncrawl_sents_path,causal_sents_path);	### Module 2: Get causal sentences from them
	get_causes_effects_line(causal_sents_path,cause_effects_path)					### Module 3: Get causes and effects
	#do_indexing_for_causes_effects_batch(cause_effects_path,given_index_name,given_doc_type)	### Module 4: Index them

def main():
	commoncrawl_sents_path = sys.argv[1]
	cleaned_commoncrawl_sents_path = sys.argv[2]
	causal_sents_path = sys.argv[3]
	cause_effects_path = sys.argv[4]
	benchmark_path = sys.argv[5]
	if(cause_effects_path.rfind('.jsonl') == -1):
		print('Cause effect output file needs to be in .jsonl format! Exiting!')
		exit()
	try:
		given_index_name = sys.argv[6]
		given_doc_type = sys.argv[7]
	except:
		given_index_name = parameter_config.index_name;
		given_doc_type = parameter_config.doctype;
	try:
		writer_mode = sys.argv[8]
	except:
		writer_mode = 'w'
	
	parameter_config.file_writer_mode = writer_mode
	single_threaded_standaldone_end_to_end_pipeline_batch(commoncrawl_sents_path,cleaned_commoncrawl_sents_path,causal_sents_path,cause_effects_path,given_index_name,given_doc_type,benchmark_path)

if __name__ == '__main__':
	main()
