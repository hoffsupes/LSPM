
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Doing setup for python dependencies in this project
"""
import sys
import subprocess

"""
Can be used in spark and as a standalone version to install libraries
"""
def do_setup_libraries(line):
	subprocess.call([sys.executable, "-m", "pip", "install",'nltk'])
	subprocess.call([sys.executable, "-m", "pip", "install",'elasticsearch'])
	subprocess.call([sys.executable, "-m", "pip", "install",'pyspark'])
	subprocess.call([sys.executable, "-m", "pip", "install",'pandas'])
	subprocess.call([sys.executable, "-m", "pip", "install",'psutil'])
	subprocess.call([sys.executable, "-m", "pip", "install",'python3'])
	subprocess.call([sys.executable, "-m", "pip", "install",'jsonlines'])
	return 1;

if __name__ == '__main__':
	do_setup_libraries();