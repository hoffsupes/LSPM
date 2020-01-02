
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

import sys
import pandas as pd
import numpy as np
import time
import nltk

"""

Benchmark scoring over various benchmarks like Semeval, NatoSFA, Risk Models and ME. Takes in a given index name and 
scores over the index associated with that name present on elasticsearch.

Various parameters described: 
given_index_name: Index name for elastisearch index, if not given default value used
benchmark_path: full path to the folder name where all the benchmarks are located, this folder is present in the repo

@exmample command line usage:

python3 crelib scoring benchmarks

"""

"""
@function to do scoring over various benchmarks like Semeval, NatoSFA, Risk Models and ME
"""
def benchmark_scoring(given_index_name,projdir,calctype='non-strict',save='no',hit_thrs=None,score_thrs=None):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
		from parameter_config import create_new_index
		from scoring_utils import outer_pool,phrase_scorer,display_max_results,display_frame

	else:
		from .config import es
		from .parameter_config import create_new_index
		from .scoring_utils import outer_pool,phrase_scorer,display_max_results,display_frame


	body = projdir + '/semeval-benchmark-v1.csv'
	df_data_1 = pd.read_csv(body)
	ce_sem = df_data_1.values;

	body = projdir + '/risk-models-benchmark-v1.csv'
	df_data_1 = pd.read_csv(body)
	ce_risk = df_data_1.values;

	ce_risk = np.array([[c[0][:c[0].find('[')].strip(' '),c[1][:c[1].find('[')].strip(' '),c[2]] for c in ce_risk])

	body = projdir + '/nato-sfa-benchmark-v1.csv'
	df_data_1 = pd.read_csv(body)
	ce_nato = df_data_1.values;
	ce_nato = np.array([[c[0].replace('\ufeff', ''),c[1].replace('\ufeff', ''),c[2].replace('\ufeff', '')] for c in ce_nato])

	body = projdir + '/ce-me-benchmark-v1.csv'
	df_data_1 = pd.read_csv(body)
	ce_me = df_data_1.values

	if(hit_thrs == None):
		hit_thrs = [0,0.5,0.6,0.65]

	if(score_thrs == None):
		score_thrs = [0]
		score_thrs.extend([x*1.0/10 for x in range(1,20) if x*1.0/10 not in score_thrs])

	t1 = time.time()

	sem_frame = pd.DataFrame();
	nato_frame = pd.DataFrame();
	me_frame = pd.DataFrame();
	risk_frame = pd.DataFrame();
	wikidata_frame = pd.DataFrame();
	iname = given_index_name

	total_lis = [(ce_sem,score_thrs,hit_thrs,iname,'word',calctype),(ce_nato,score_thrs,hit_thrs,iname,'phrase',calctype),(ce_me,score_thrs,hit_thrs,iname,'phrase',calctype),(ce_risk,score_thrs,hit_thrs,iname,'phrase',calctype)] #,(ce_wikidata,score_thrs,hit_thrs,iname,'phrase','non_causal')];

	try:
	    pool = outer_pool(processes = len(total_lis))		## Multiprocessing to make scoring simpler
	    poolputs = pool.starmap(phrase_scorer, total_lis)	## Batch processing within elastisearch on top of that for even faster use
	finally: 
	    pool.close()
	    pool.join()

	[sem_framet,nato_framet,me_framet,risk_framet] = poolputs;

	_,sem_frame = sem_framet;
	_,nato_frame = nato_framet;
	_,me_frame = me_framet;
	_,risk_frame = risk_framet;

	print('Semeval')
	print(display_max_results(sem_frame,'SemEval'))

	print('Nato')
	print(display_max_results(nato_frame,'NatoSFA'))

	print('ME')
	print(display_max_results(me_frame,'ME'))

	print('Risk')
	print(display_max_results(risk_frame,'Risk Drivers'))

	t2 = time.time()

	print("Time taken ",t2-t1)

	if(save == 'yes'):
		sfa = display_max_results(sem_frame,'SemEval')
		natf = display_max_results(nato_frame,'NatoSFA')
		mef = display_max_results(me_frame,'ME')
		rif = display_max_results(risk_frame,'Risk Drivers')
		outtup = (sfa,natf,mef,rif);

		import pickle
		try:
			import os
			os.mkdir('results')
		except:
			pass;
		with open('results/'+projdir+calctype+given_index_name+'.pkl','wb') as outf:
			pickle.dump(outtup,outf)

def benchmark_scoring_custom(given_index_name,ce_path,name,calctype='non-strict',save='no',hit_thrs=None,score_thrs=None):
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
		from parameter_config import create_new_index
		from scoring_utils import outer_pool,phrase_scorer,display_max_results,display_frame,phrase_scorer_non_bulk

	else:
		from .config import es
		from .parameter_config import create_new_index
		from .scoring_utils import outer_pool,phrase_scorer,display_max_results,display_frame,phrase_scorer_non_bulk

	df_data_1 = pd.read_csv(ce_path)
	ce_data = df_data_1.values;

	if(hit_thrs == None):
		hit_thrs = [0,0.5,0.6,0.65]

	if(score_thrs == None):
		score_thrs = [0]
		score_thrs.extend([x*1.0/10 for x in range(1,20) if x*1.0/10 not in score_thrs])

	t1 = time.time()

	data_frame = pd.DataFrame();
	# data_framet = phrase_scorer(ce_data,score_thrs,hit_thrs,given_index_name,'phrase',calctype)
	data_framet = phrase_scorer_non_bulk(ce_data,score_thrs,hit_thrs,given_index_name,name,'phrase',calctype)
	_,data_frame = data_framet;
	# lll = 0;
	# for h in hit_thrs:
	# 	for scc in score_thrs:
	# 		_,dat = scoring_phrases(es,ce_data,given_index_name,scc,h,'phrase')
	# 		data_frame = data_frame.append(pd.DataFrame(dat,index=[lll]))
	# 		lll+=1;

	print(name)
	print(display_max_results(data_frame,name))

	t2 = time.time()

	print("Time taken ",t2-t1)

	if(save == 'yes'):
		sfa = display_max_results(data_frame,name)

		import pickle
		try:
			import os
			os.mkdir('results')
		except:
			pass;
		with open('results/'+calctype+given_index_name+name+'.pkl','wb') as outf:
			pickle.dump(sfa,outf)

if __name__ == '__main__':
	parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		import parameter_config
	else:
		from . import parameter_config
	
	try:
		given_index_name = sys.argv[2];
	except:
		given_index_name = parameter_config.index_name
	benchmark_path = sys.argv[1];
	if(benchmark_path[-1]=='/'):
		benchmark_path = benchmark_path[:-1];
	try:
		calctype = sys.argv[3]
	except:
		calctype = 'non-strict'
	try:
		save = sys.argv[4]
	except:
		save = 'no'
	benchmark_scoring(given_index_name,benchmark_path,calctype,save)