
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
@Spark intermediate files
"""
import sys
import setup_script
from pyspark import SparkConf, SparkContext
conf = SparkConf()
conf = conf.set('spark.executor.instances','3')
sc = SparkContext(conf=conf)
execs = sc._conf.get('spark.executor.instances')
li = [1]*int(execs);
rddsetup = sc.parallelize(li,int(execs)).map(setup_script.do_setup_libraries)
