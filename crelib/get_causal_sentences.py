
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""

Get sentences from a TEXT file / text corpus with sentences present line by line and OUTPUT another TEXT file which contains a list of causal sentences line by line

Various parameters described: 
inpath: Output path to cleaned corpus text file (.txt file)
outpath: Output path to file which contains all the causal sentences from the previous file (.txt file)

@example command line usage:

python3 crelib causalsent cleaned_test_file.txt causal.txt

"""

import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	from causal_identification import get_all_cause_effects,get_causal_sentences_only
	from parameter_config import file_writer_mode
else:
	from .causal_identification import get_all_cause_effects,get_causal_sentences_only
	from .parameter_config import file_writer_mode

"""
Given an input txt file, read all lines and output causal sentences into another text file
"""
def get_causal_sentences_lines(inpath,outpath):
	filereader = open(inpath,'r')
	filewriter = open(outpath,file_writer_mode)

	for line in filereader:
		clines = get_causal_sentences_only([line])
		if(len(clines)):
			filewriter.write(line+'\n')

	filewriter.close()
	filereader.close()

"""
@Spark intermediate function: to get causal senteces from one file
"""
def get_causal_sent_one(sent):
	causal_sent = get_causal_sentences_only([sent])
	return causal_sent;

"""
main()
"""
def main():
	inpath = sys.argv[1];
	outpath = sys.argv[2];
	get_causal_sentences_lines(inpath,outpath)	

if __name__ == '__main__':
	main()
