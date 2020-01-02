
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""

Ingest a TEXT file which has a corpus present which contains sentences line by line.
Cleans it on basis of removal of stray HTML characters and also remove paragraphs which may have creeped in. Ouptuts another TEXT file.

Various parameters described: 
inpath: Path to the input text corpus file (.txt file)
outpath: Output path to cleaned corpus text file (.txt file)

@example command line usage:

python3 crelib/ingest_corpus.py input_test_data.txt cleaned_test_file.txt

OR

python3 crelib ingest input_test_data.txt cleaned_test_file.txt

"""

import sys
import re
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	from cleaner import cleanr,word_thresh
	from parameter_config import file_writer_mode
else:
	from .parameter_config import file_writer_mode
	from .cleaner import cleanr,word_thresh

"""
Takes in input text file and cleans it with simple operations and outputs into another text file
"""
def ingest_corpus(inpath,outpath):
	filereader = open(inpath,'r')
	filewriter = open(outpath,file_writer_mode)

	for line in filereader:
	    if type(line) != type('str'):
	        line = line.decode('utf-8')
	    if(len(line) > word_thresh or len(line) == 0):
	        continue;
	    line = re.sub(cleanr, '',line).replace('\n','');
	    filewriter.write(line+'\n')

	filewriter.close()
	filereader.close()

def main():
	inpath = sys.argv[1];
	outpath = sys.argv[2];
	ingest_corpus(inpath,outpath)

if __name__ == '__main__':
	main()
