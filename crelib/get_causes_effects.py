
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""

Get causes and effects from a list of causal sentences present in a text file. INPUT is a TXT file, OUTPUT is a JSONL file.

Various parameters described: 

inpath: Input path to file which contains all the causal sentences from the previous file (.txt file)
outpath: Output path to file which contains all the cause effect pairs from the previous file (.jsonl file)

@example command line usage:

python3 crelib/get_causes_effects.py causal.txt cause_effects.jsonl

OR

python3 crelib causeeffect causal.txt cause_effects.jsonl

"""

import sys
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	from causal_identification import get_all_cause_effects
	from parameter_config import file_writer_mode
else:
	from .causal_identification import get_all_cause_effects
	from .parameter_config import file_writer_mode
import subprocess
import jsonlines
import os.path

"""
Take causal sentences present in a text file and get cause effect pairs present in a jsonl file as ouptut
"""
def get_causes_effects_line(inpath,outpath):
	filereader = open(inpath,'r')
	jsonfilemode = 'w'
	if(os.path.isfile(outpath) and file_writer_mode != 'w'):
		jsonfilemode = 'a'

	with jsonlines.open(outpath, mode=jsonfilemode) as writer:
		for line in filereader:
			ceff = get_all_cause_effects([line])
			if(len(ceff.keys())):
				keyval = list(ceff.keys())[0]
				writer.write({'cause':ceff[keyval]['cause'],'effect':ceff[keyval]['effect'],'evidences':[line.strip()]})

	filereader.close()

"""
@Spark intermediate function: Get cause effect for one causal sentence
"""
def get_cause_effect_one(causal_sent):
	ceff = get_all_cause_effects([causal_sent])
	keyval = list(ceff.keys())[0]
	return {'cause':ceff[keyval]['cause'],'effect':ceff[keyval]['effect'],'evidences':ceff[keyval]['evidences']}

"""
@Spark intermediate function: Get an iterator of cause effects from a number of causal sentences
"""
def get_cause_effect_partition(causal_sents):
	ceff = get_all_cause_effects(causal_sents);
	retvalue = [{'cause':ceff[keyval]['cause'],'effect':ceff[keyval]['effect'],'evidences':ceff[keyval]['evidences']} for keyval in ceff.keys()]
	return iter(retvalue)

def main():
	inpath = sys.argv[1];
	outpath = sys.argv[2];
	get_causes_effects_line(inpath,outpath)

if __name__ == '__main__':
	main()
