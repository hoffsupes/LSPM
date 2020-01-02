
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################


"""
Various preprocessing functions and utilities
"""


import sys
import re
import nltk

cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
word_thresh = 500;

########################################################################################################################
######################### clean paragraphs of text and lines

def clean_para(uncleaned_para):
    lines = [re.sub(cleanr, '',s).replace('\n','') for s in sent_tokenize(uncleaned_para)]
    lines = [line.decode('utf-8') if type(line) != type('str') else line for line in lines]
    lines = [line.strip() for line in lines if len(line) < word_thresh and len(line) != 0]
    return lines;

def clean_lines(lines):
#     lines = [re.sub(cleanr, '',s).replace('\n','') for s in sent_tokenize(lines)]
    lines = [line.decode('utf-8') if type(line) != type('str') else line for line in lines]
    lines = [re.sub(cleanr, '',line).replace('\n','').strip() for line in lines if len(line) < word_thresh and len(line) != 0]
    return lines;

def sentence_obtainment(obj_json):
    sents = []
    sents += [obj_json['headline']]
    summary = obj_json['summary']
    if(len(summary)):
        sents += clean_para(summary)
    return sents;

def sentence_converter3(obj_json):
    sents = []
    sents += obj_json['headline']
    # print(obj_json)
    summary = obj_json['summlines']
    sents += clean_lines(summary)
    return sents;

def sentence_converter2(obj_json,outfile,mode='non_corpus_index',iname=None):
    sents = []
    sents += obj_json['headline']
    # print(obj_json)
    summary = obj_json['summlines']
    sents += clean_lines(summary)
    if(mode == 'corpus_index'):
        index_corpus(sents,iname)
    wri = open(outfile,'a+')
    for line in sents:
        try:
            if(type(line)!=type('str')):
                line = line.decode('utf-8')
            wri.write(line.strip() + '\n')
        except Exception as E:
            print('Error in writing sentence converter 2 ',E)
            pdb.set_trace()
    wri.close()
    return 1;

######################### 
########################################################################################################################