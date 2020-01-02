
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

import jsonlines
import sys

def process_jsonfile(filename):
	with jsonlines.open(filename,'r') as filew:
		lines = [str(line) for line in filew]
	newfilename = filename[:filename.rfind('.jsonl')] + '_unique.jsonl'
	lines = list(set(lines))
	newlines = [eval(line) for line in lines]
	with jsonlines.open(newfilename,'w') as filenw:
		filenw.write_all(newlines)

def process_txtfile(filename):
	with open(filename,'r') as filer:
		lines = [line.strip() for line in filer]
	lines = list(set(lines))
	newfilename = filename[:filename.rfind('.txt')] + '_unique.txt'
	with open(newfilename,'w') as filenw:
		[filenw.write(line + '\n') for line in lines]

def main():
	filename = sys.argv[1]
	if('.jsonl' in filename):
		process_jsonfile(filename)
	elif('.txt' in filename):
		process_txtfile(filename)
	else:
		print('File must be jsonlines or text file!')
		print('Please try again!')
		exit()

if __name__ == '__main__':
	main()
