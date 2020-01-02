
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
@Spark version: Tested on spark-2.4.4 on a spark cluster set up with 4 docker containers (1 master and 3 slaves / executors) 
"""

import sys
from pyspark import SparkConf, SparkContext
import subprocess
subprocess.call([sys.executable, "-m", "pip", "install",'jsonlines'])
import setup_script
import get_causes_effects
import causal_identification
import index_pairs

# os.chdir('/tmp/')
# print(os.getcwd())
# print(listdir('/tmp/'))

conf = SparkConf()
conf = conf.set('spark.executor.instances','3')
sc = SparkContext(conf=conf)

#sc.addPyFile("test_data.txt")
#sc.addPyFile("/tmp/lspm_deps.zip")

#execs = sc._conf.get('spark.executor.instances')
#li = [1]*int(execs);
#rddsetup = sc.parallelize(li,int(execs)).map(setup_script.do_setup_libraries)

#sys.path.append('..')

# inputtextfilepath = sys.argv[1]; #### input file path (should be present in the driver)
# outputfilepath = sys.argv[2]; #### stocator file path
# logfilename = sys.argv[3];    #### will be stored on stocator
# try:
# 	use_stocator = sys.argv[4];
# except:
# 	if('cos://' in outputfilepath or 'cos://' in inputtextfilepath or 'cos://' in logfilename):
# 		print('Please add option stocator at end of program call to use stocator / IBM cloud based storage')
# 		exit(1)
# 	pass

inputtextfilepath = 'file:///input_test_data.txt'; #### input file path (should be present in the driver)
causal_sents_out = 'file:///causal_sents_out_new_path.txt'; #### causal sentences out path
cause_effect_out = 'file:///cause_effect_out_new_path.txt'; #### causal sentences out path
# logfilename = 'logtest.txt';    #### will be stored on stocator
use_stocator = 'no';

# print(inputtextfilepath)
# print(outputfilepath)
# print(logfilename)
# print(use_stocator)
# line = ["2017-09-25 06:33:02  970273953 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160917165637-00025.warc.gz","2017-09-25 06:33:50 1073793640 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160918165637-00026.warc.gz","2017-09-25 06:34:26 1073755152 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160919125823-00027.warc.gz","2017-09-25 06:34:54 1073764846 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160920065328-00028.warc.gz","2017-09-25 06:35:23 1062977537 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160920205428-00029.warc.gz","2017-09-25 06:35:52 1073782282 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160921141810-00000.warc.gz","2017-09-25 06:36:20 1073742763 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160926211809-00000.warc.gz","2017-09-25 06:36:48 1030170196 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160927074341-00000.warc.gz","2017-09-25 06:37:16   43598787 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160928074341-00001.warc.gz","2017-09-25 06:37:18  958045652 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160928075927-00002.warc.gz","2017-09-25 06:37:46  115721849 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160929075927-00003.warc.gz","2017-09-25 06:38:00  959611752 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160929101044-00004.warc.gz","2017-09-25 06:38:25  114141481 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160930101058-00005.warc.gz","2017-09-25 06:38:33  784668188 crawl-data/CC-NEWS/2016/09/CC-NEWS-20160930122238-00006.warc.gz","2017-09-25 07:09:01  289093282 crawl-data/CC-NEWS/2016/10/CC-NEWS-20161001122244-00007.warc.gz"]
# linein = line[0:3];
# rdd = sc.textFile(inputtextfilepath)
from input_data_list import sentence_list			## Hard to give input to docker


###########################################################################################
###########################################################################################
###########################################################################################
### from stocator_config import stoc_config	## When running on the IBM cloud
# eval(stoc_config)
# rdd = sc.parallelize('cos:///bucket_name.s3/yourfilename_on_cloud_here.txt').distinct()
###########################################################################################
###########################################################################################
###########################################################################################
print('\noriginal sentence list:',sentence_list,'\n');

### Going from original sentence list to looking for only distinct instances ---> mapPartitions (causal identification) ----> mapPartitions (causes and effects) -----> mapPartitions(indexing)

### I'm forcing a call to collect just to show you the output at intermediate stages, in this case getting causes and effects from the large sentence list, (this can obviously be skipped by calling saveAsTextFile which I'm also doing, just doing this extra step (collect) to show you what's going on in the middle of the pipeline)

## That's the result from collect (after collecting all the cause effect pairs from the worker nodes)'

rdd = sc.parallelize(sentence_list).distinct()
#rdd = sc.textFile('/tmp/test_data.txt').distinct()
rdd3 = rdd.mapPartitions(causal_identification.get_causal_sentences_only_iter)
print(' The type of the result you get from causal sentence identification is ',type(rdd3))
# print(rdd3)
# rddn = sc.parallelize(rdd3).collect
try:
	rdd3.saveAsTextFile(causal_sents_out)
except:
	import time
	rdd3.saveAsTextFile(causal_sents_out + '_' + str(time.time()) + '.txt')

rddli = rdd3.mapPartitions(get_causes_effects.get_cause_effect_partition).collect()

print('\n\n',rddli,'\n\n')
rdd4 = sc.parallelize(rddli)

try:
	rdd4.saveAsTextFile(cause_effect_out);
except:
	import time
	rdd4.saveAsTextFile(cause_effect_out + '_' + str(time.time()) + '.txt')

# rdd4.saveAsTextFile(cause_effect_out);

ncount = rdd4.map(lambda x, :(x,'cause_effect_spark_testing_going_through','cause_effect_pairs')).mapPartitions(index_pairs.do_indexing_many).count()
print('Sentences processed:',ncount)
