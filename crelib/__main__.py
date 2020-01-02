
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
	import setup_script
	import parameter_config
	import ingest_corpus
	import get_causal_sentences
	import get_causes_effects
	import index_pairs
	import benchmark_scorer
	import binary_causal_question_answering
	import standalone_single_threaded_version
	import create_subnetwork
else:
	from . import setup_script
	from . import parameter_config
	from . import ingest_corpus
	from . import get_causal_sentences
	from . import get_causes_effects
	from . import index_pairs
	from . import benchmark_scorer
	from . import binary_causal_question_answering
	from . import standalone_single_threaded_version
	from . import create_subnetwork

## ingest corpus
def do_the_ingest_corpus():
	inpath = sys.argv[2];
	outpath = sys.argv[3];
	ingest_corpus.ingest_corpus(inpath,outpath)

## causal sentence identification
def do_the_causal_sentences():
	inpath = sys.argv[2];
	outpath = sys.argv[3];
	get_causal_sentences.get_causal_sentences_lines(inpath,outpath)	

## cause effect extraction
def do_the_causes_effects():
	inpath = sys.argv[2];
	outpath = sys.argv[3];
	get_causes_effects.get_causes_effects_line(inpath,outpath)

## index the cause effect pairs
def do_the_index_pairs():
	inpath = sys.argv[2];

	try:
		given_index_name = sys.argv[3];	
		given_doc_type = sys.argv[4];
	except:
		given_index_name = parameter_config.index_name;
		given_doc_type = parameter_config.doctype;
	index_pairs.do_indexing_for_causes_effects_direct(inpath,given_index_name,given_doc_type)	

## score on all benchmarks
def do_the_benchmark_scoring():	
	try:
		given_index_name = sys.argv[3];
	except:
		given_index_name = parameter_config.index_name
	print(given_index_name)
	benchmark_path = sys.argv[2];
	try:
		option = sys.argv[4];
	except:
		option = 'non-strict'
	if(benchmark_path[-1]=='/'):
		benchmark_path = benchmark_path[:-1];
	benchmark_scorer.benchmark_scoring(given_index_name,benchmark_path,option)	

## perform BINARY CAUSAL QUESTION ANSWERING task
def do_the_bcqa():
	try:
		given_index_name = sys.argv[2]
	except:
		given_index_name = parameter_config.index_name
	binary_causal_question_answering.bcqa(given_index_name)

## standalone_single_threaded_version
def do_the_pipeline():
	commoncrawl_sents_path = sys.argv[2]
	cleaned_commoncrawl_sents_path = sys.argv[3]
	causal_sents_path = sys.argv[4]
	cause_effects_path = sys.argv[5]
	benchmark_path = sys.argv[6]
	if(cause_effects_path.rfind('.jsonl') == -1):
		print('Cause effect output file needs to be in .jsonl format! Exiting!')
		exit()
	try:
		given_index_name = sys.argv[7]
		given_doc_type = sys.argv[8]
	except:
		given_index_name = parameter_config.index_name;
		given_doc_type = parameter_config.doctype;

	standalone_single_threaded_version.single_threaded_standaldone_end_to_end_pipeline(commoncrawl_sents_path,cleaned_commoncrawl_sents_path,causal_sents_path,cause_effects_path,given_index_name,given_doc_type,benchmark_path)

## usage instructions in case the user enters something abusive / wrong
def non_usage_display():
	print('\n\nUsage python3 <Usage mode> <additional command line options>')
	print("Usage modes:\n\n \tingest: Ingest data\n\tpipeline: Complete pipeline (run all modules) \n\tbcqa: Binary Causal Question Answering \n\tscoring: Scoring on all benchmarks\n\tindex: Indexing\n\tcausalsent: Causal sentence identiication\n\tcauseeffect: Cause effect extraction")
	print('\nExamples:\n\ningest: \npython3 crelib ingest /full/path/to/input_text_corpus /full/path/to/cleaned_corpus_text_file')
	print('\n\ncausalsent:\npython3 crelib causalsent /full/path/to/cleaned_corpus_text_file /full/path/to/causal_sentences_text_file')
	print('\n\ncauseeffect:\npython3 crelib causeeffect /full/path/to/causal_sentences_text_file /full/path/to/cause_effect_json_file')
	print('\n\nindex:\npython3 crelib index /full/path/to/input_cause_effect_json_file optional_value_index_name optional_value_doctype')
	print('\n\nscoring:\npython3 crelib scoring /full/path/to/benchmarks_folder optional_index_name')
	print('\n\nbcqa:\npython3 crelib bcqa optional_index_name ')
	print('\n\npipeline:\npython3 crelib pipeline /full/path/to/input_text_corpus /full/path/to/cleaned_corpus_text_file /full/path/to/causal_sentences_text_file /full/path/to/cause_effect_json_file /full/path/to/benchmarks_folder optional_value_index_name optional_value_doctype')
	

try:
	usage_option = sys.argv[1]
except:
	non_usage_display();
	exit()

if(usage_option == 'ingest'):
	do_the_ingest_corpus();
elif(usage_option == 'pipeline'):
	do_the_pipeline();
elif(usage_option == 'bcqa'):
	do_the_bcqa();
elif(usage_option == 'scoring'):
	do_the_benchmark_scoring();
elif(usage_option == 'index'):
	do_the_index_pairs();
elif(usage_option == 'causalsent'):
	do_the_causal_sentences();
elif(usage_option == 'causeeffect'):
	do_the_causes_effects();
else:
	non_usage_display();
	exit(1)
