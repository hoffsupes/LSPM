
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Various scoring functions or functions or classes related to scoring.
"""

import math
import multiprocessing
import multiprocessing.pool
import sys
import nltk
import os

parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    import parameter_config
    from parameter_config import create_new_index
else:
    from . import parameter_config
    from .parameter_config import create_new_index
maxSents = -1;
sentChunkNumber = 3000;

#@function score entire phrases
def scoring_phrases(es,CE,index_name,thresh=1,hthresh=2,typecall='word',scoring='causal'):
    # SE = [];
    scor = {};
    tp,tn,fp,fn = [0,0,0,0]
    
    tot = len(CE)
    N = int(0.1*tot)
    for ii,c in enumerate(CE):
        score = 0;
        pscore = 0;
        try:
            c = c.tolist()
            score=0

            if(c[0]==float('nan') or c[1]==float('nan') or c[2] == float('nan')):
                continue;
            if(c[0] == 'NullPointerException' or c[1] == 'NullpointerException'):
                continue;
            if typecall == 'word':
                cause_cand,effect_cand = [[c[0]],[c[1]]]
            else:
                cause_cand,effect_cand = pross_ce_phrase(c[0],c[1]) 
            fhits = form_evidence_query(es,index_name,cause_cand,effect_cand)['total']
            rhits = form_evidence_query(es,index_name,effect_cand,cause_cand)['total']
            # chits = form_co_occurance_query(es,parameter_config.corpus_index_name,cause_cand,effect_cand)['total']
            if(fhits):
                score = (fhits+1.0)/(rhits+1.0);
                # pscore = (chits + 1.0) / (rhits + fhits + 1.0);
            else:
                score = 0;
                # pscore = 0;
            if scoring ==  'causal':
                [tp,fp,fn,tn] = get_true_false(fhits,score,thresh,hthresh,tp,fp,fn,tn,c)
                # SE.append([c[0],c[1],score])
            # else:
            #     [tp,fp,fn,tn] = get_true_false(fhits,pscore,thresh,hthresh,tp,fp,fn,tn,c)
            #     SE.append([c[0],c[1],pscore])
            if(ii%N == 0):
                print(os.getppid(),'_PPID_',os.getpid(),'_PID_',hthresh,' threshold1 ',thresh,' threshold2 ',ii/(tot*1.0)*100,'% done!')
        except Exception as E:
            print(E)
            print(c)
    total_len = len(CE);

    if(tp+tn+fp+fn != 0):
        scor['accuracy'] = (tp+tn)/float(tp+tn+fp+fn)
    else:
        scor['accuracy'] = (tp+tn)/float(total_len)

    
    if(tp+fp == 0):
        scor['precision'] = 0;
    else:
        scor['precision'] = (tp)/float(tp+fp)
    
    if((tp+fn) == 0):
        scor['recall'] = 0;
    else:
        scor['recall'] = (tp)/float(tp+fn)
        
    scor['tp'] = tp
    scor['tn'] = tn
    scor['fp'] = fp
    scor['fn'] = fn
    scor['th1'] = thresh
    scor['th2'] = hthresh
    if(scor['precision']+scor['recall'] == 0):
        scor['F1'] = 0
    else:
        scor['F1'] = (2*scor['precision']*scor['recall'])/(scor['precision']+scor['recall'])  

    return scor;

"""
@utility function: Single threaded scoring helper, does network lookups in one go 
"""
def modify_to_get_feq(es,CE,index_name,typecall='word',scoring='causal'):
    # SE = [];
    scor = {};
    tp,tn,fp,fn = [0,0,0,0]
    
    tot = len(CE)
    N = int(0.1*tot)
    fhitsli = []
    rhitsli = []
    for ii,c in enumerate(CE):
        try:
            c = c.tolist()
            score=0

            if(c[0]==float('nan') or c[1]==float('nan') or c[2] == float('nan')):
                continue;
            if(c[0] == 'NullPointerException' or c[1] == 'NullpointerException'):
                continue;
            if typecall == 'word':
                cause_cand,effect_cand = [[c[0]],[c[1]]]
            else:
                cause_cand,effect_cand = pross_ce_phrase(c[0],c[1]) 
            fhits = form_evidence_query(es,index_name,cause_cand,effect_cand)['total']
            rhits = form_evidence_query(es,index_name,effect_cand,cause_cand)['total']
            fhitsli.append(fhits)
            rhitsli.append(rhits)
            if(ii%N == 0):
                print(ii/(tot*1.0)*100,'% done!')
        except Exception as E:
            print(E)
            print(c)
    fhitsli = np.array(fhitsli);
    rhitsli = np.array(rhitsli);
    outli = (fhitsli,rhitsli,[])
    return outli;

#@function get various accuracy metrics, true positives, false positives, true negatives, false negatives
def get_true_false(hits,score,thresh,hthresh,tp,fp,fn,tn,c,op='strict'):
    if(score and op == 'strict'):
        if float(score) >= thresh and hits >= hthresh:
            if c[2].strip(' ').lower() == 'causal':
                tp+=1
            else:
                fp+=1;
        else:
            if c[2].strip(' ').lower() == 'non_causal':
                tn+=1;
            else:
                fn+=1;
    if(op != 'strict'):
        if float(score) >= thresh and hits >= hthresh:
            if c[2].strip(' ').lower() == 'causal':
                tp+=1
            else:
                fp+=1;
        else:
            if c[2].strip(' ').lower() == 'non_causal':
                tn+=1;
            else:
                fn+=1;        
    return tp,fp,fn,tn;


"""
break standard multisearch in parts
"""
def do_msearch_parts(es,body,batch_size=2000):
    tot= len(body)
    total_resp = {"responses":[]}
    b = 0;
    tem = [];
    for i in range(2,tot+2,2):
        tem.extend(body[i-2:i])
        if(len(tem) == batch_size):
            resp = es.msearch(body = tem)
            total_resp["responses"] += resp["responses"];
            print(b,' batch done!')
            b+=1;
            tem = [];
    if(len(tem)):
        resp = es.msearch(body = tem)
        total_resp["responses"] += resp["responses"]
        tem = [];
    return total_resp;


#@function perform batch / bulk search query with N retries, where,  N = parameter_config.trystopper  
def get_resp_msearch(es,body,break_parts=False):
    tryvar = 1;
    while(tryvar<=parameter_config.trystopper):
        try:
            if(break_parts):
                resp = do_msearch_parts(es,body)
            else:
                resp = es.msearch(body = body)
            oldvar = tryvar;
            if('responses' not in resp.keys()):
                tryvar = oldvar;
                time.sleep(tryvar*0.1)
                continue;
            elif(len([r for r in resp['responses'] if (r['status']!=200 or r['timed_out'] == True)])):
                tryvar = oldvar;
                time.sleep(tryvar*0.1)
                continue;
            break;
        except Exception as E:
            print('get resp msearch',E)
            print('trying',parameter_config.trystopper-tryvar,' times more')
            tryvar+=1;
            time.sleep(tryvar*0.1)
    if(tryvar > parameter_config.trystopper):
        print('failed to do batch search')
        return 0;
    return resp;

#@function perform simple search query with N retries, where,  N = parameter_config.trystopper
def get_resp_index(indexname,bodyname,es):
    tryvar = 1;
    while(tryvar<=parameter_config.trystopper):
        try:
            resp = es.search(index=indexname, body=bodyname)
            oldvar = tryvar;
            
            if(resp['timed_out']):
                tryvar = oldvar;
                time.sleep(tryvar*0.1)
                continue;
            break
        except Exception as E:
            tryvar+=1;
            time.sleep(tryvar*0.1)
    if(tryvar > parameter_config.trystopper):
        print(' failed to do search')
        return 0
    return resp;

#@function get bulk query to search for
def create_msearch(es, index, cause_keywords, effect_keywords,total_request,calltype='evidence',start=0, sample_size=9000):
    if(calltype=='evidence'):
        req_head = {'index': index}#, 'type':'cause_effect_pairs'}
        query = get_evidence_query(es, index, cause_keywords, effect_keywords);
    else:
        req_head = {'index': parameter_config.corpus_index_name}#, 'type':'headlines'}
        query = get_co_occurance_query(es, index, cause_keywords, effect_keywords);
    total_request.extend([req_head,query]);
    return total_request;

#@function perform a bulk query after collecting it into one large json object
def do_query_block(es, index, cepairs,calltype='evidence'):

    total_request = [];
    for ce in cepairs:
        cause_keywords, effect_keywords = ce[0],ce[1];
        total_request = create_msearch(es, index, cause_keywords, effect_keywords,total_request,calltype);
    large_response = get_resp_msearch(es,total_request);
    return large_response;

#@function get one large json object for a bulk query
def get_query_block(es, index, cepairs,calltype='evidence'):

    total_request = [];
    for ce in cepairs:
        cause_keywords, effect_keywords = ce[0],ce[1];
        total_request = create_msearch(es, index, cause_keywords, effect_keywords,total_request,calltype);
#     large_response = get_resp_msearch(total_request);
    return total_request;

#@function get body for performing a cause effect index elastisearch query
def get_evidence_query(es, index, cause_keywords, effect_keywords, start=0, sample_size=9000):
    sbool = {}
    shoulds = []
    for cause in cause_keywords:
        for effect in effect_keywords:
            mbool = {
                "must" : [
                    {"match_phrase": {"cause": cause.lower()} },
                    {"match_phrase": {"effect": effect.lower()}},
                ]
            }
            shoulds.append({"bool" : mbool})
    sbool['should'] = shoulds
    query = { "bool" : sbool}
    body = {
        "query": query,
        "from": start,
        "size": sample_size
    }
    return body;

#@function get body for performing the co-occurance (corpus, p_causal) elastisearch query
def get_co_occurance_query(es, index, cause_keywords, effect_keywords, start=0, sample_size=9000):
    sbool = {}
    shoulds = []
    for cause in cause_keywords:
        for effect in effect_keywords:
            mbool = {
                "must" : [
                    {"multi_match" : { "query": cause.lower()+" "+effect.lower(), "fields": ["headline"], "type": "phrase", "slop": 1000 }}
                ]
            }
            shoulds.append({"bool" : mbool})
    sbool['should'] = shoulds
    query = { "bool" : sbool}
    body = {
        "query": query,
        "from": start,
        "size": sample_size
    }
    return body

def form_evidence_query(es, index, cause_keywords, effect_keywords, start=0, sample_size=9000):
    # from config import es
    sbool = {}
    shoulds = []
    for cause in cause_keywords:
        for effect in effect_keywords:
            mbool = {
                "must" : [
                    {"match_phrase": {"cause": cause.lower()} },
                    {"match_phrase": {"effect": effect.lower()}},
                ]
            }
            shoulds.append({"bool" : mbool})
    sbool['should'] = shoulds
    query = { "bool" : sbool}
    body = {
        "query": query,
        "from": start,
        "size": sample_size
    }
    res = get_resp_index(index,body,es)
#     res = es.search(index=index, body=body)
    return res['hits']

#@function perform the co-occurance (corpus or p_causal) elastisearch query
def form_co_occurance_query(es, index, cause_keywords, effect_keywords, start=0, sample_size=9000):
    # from config import es
    sbool = {}
    shoulds = []
    for cause in cause_keywords:
        for effect in effect_keywords:
            mbool = {
                "must" : [
                    {"multi_match" : { "query": cause.lower()+" "+effect.lower(), "fields": ["headline"], "type": "phrase", "slop": 1000 }}
                ]
            }
            shoulds.append({"bool" : mbool})
    sbool['should'] = shoulds
    query = { "bool" : sbool}
    body = {
        "query": query,
        "from": start,
        "size": sample_size
    }
    res = get_resp_index(index,body,es)
    return res['hits']

"""
functions related to chunking and processing phrases
"""

npchunks_grammar = r"""
          NP: {<NNP>+<POS>?<NN|NNS>+}              # chunk sequences of proper nouns
              {<DT|PP\$>?<JJ|JJR|JJS>*<NN|NNS>+}   # chunk determiner/possessive, adjectives and noun
          """
npchunks_cp = nltk.RegexpParser(npchunks_grammar)

nounonly_chunks_grammar = r"""
          NP: {<NNP>+<POS>?<NN|NNS>+}              # chunk sequences of proper nouns
              {<NN|NNS>+}   # chunk determiner/possessive, adjectives and noun
          """
nounonly_chunks_cp = nltk.RegexpParser(nounonly_chunks_grammar) 

def get_phrases_nltk(input):
    out = set()
    chunks = npchunks_cp.parse(nltk.pos_tag(nltk.word_tokenize(input)))
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            out.add(' '.join(c[0] for c in chunk.leaves()))
    chunks = nounonly_chunks_cp.parse(nltk.pos_tag(nltk.word_tokenize(input)))
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            out.add(' '.join(c[0] for c in chunk.leaves()))
    return list(out)

def get_chunks(input, method="nltk"):
    if method=="nltk":
        out = []
        chunks = npchunks_cp.parse(nltk.pos_tag(nltk.word_tokenize(input)))
        for chunk in chunks:
            if hasattr(chunk, 'label'):
                out.append(' '.join(c[0] for c in chunk.leaves()))
        return out
    elif method=="nltk_nouns_only":
        out = []
        chunks = nounonly_chunks_cp.parse(nltk.pos_tag(nltk.word_tokenize(input)))
        for chunk in chunks:
            if hasattr(chunk, 'label'):
                out.append(' '.join(c[0] for c in chunk.leaves()))
        return out
    elif method=="none":
        return [input]

def pross_ce_phrase(cphrase,ephrase):
    causes = get_phrases_nltk(cphrase);
    effects = get_phrases_nltk(ephrase);
    extended_causes = list(set(causes));
    extended_effects = list(set(effects));
    return extended_causes,extended_effects

def get_chunks_batch(CE):
    celist = [];
    cerevlist = [];
    for c in CE:
        cause_cand,effect_cand = pross_ce_phrase(c[0],c[1])
        celist.append([cause_cand,effect_cand]);
        cerevlist.append([effect_cand,cause_cand])
    return celist,cerevlist;

#@function get accuracy metrics but for a bulk of data at once
def get_true_false_array(inli,labs,thresh,hthresh,tp,fp,fn,tn,scoring='causal',op='strict'):
    
    fhits,rhits,chits = inli
    
    nonzerof = np.asarray(fhits>0,float)
    if(scoring == 'causal'):
        slist = ((chits + 1.0) / (rhits + fhits + 1.0))*nonzerof
    else:    
        slist = ((fhits+1) / (rhits+1))*nonzerof
    
    if(op == 'strict'):
        nzs = slist!=0;
        slist = slist[nzs]
        fhits = fhits[nzs];
        labs = labs[nzs]
        slist = slist*np.asarray(slist>0,float);
    
    
    causal_logical = labs == 'causal';## actually causal
    score_logical = np.logical_and(np.asarray(slist >= thresh,float),np.asarray(fhits >= hthresh,float));   ## found to be causal
    non_causal_logical = labs != 'causal';## actually non causal
    score_logical_not = np.logical_not(score_logical);   ## found to be non causal
    
    tp = sum(np.logical_and(causal_logical,score_logical),0)
    fp = sum(np.logical_and(non_causal_logical,score_logical),0)
    fn = sum(np.logical_and(causal_logical,score_logical_not),0)
    tn = sum(np.logical_and(non_causal_logical,score_logical_not),0)
    
    return tp,fp,fn,tn;

#@function do scoring but on a bulk of data at once
def score_bulker(inli,labels,thresh=1,hthresh=2,scoring='causal',calc_type='non_strict'):
    scor = {};
    tp,tn,fp,fn = [0,0,0,0]   
    tp,fp,fn,tn = get_true_false_array(inli,labels,thresh,hthresh,tp,fp,fn,tn,scoring,calc_type)  
    total_len = len(labels);
#     print(total_len)
    if(tp+tn+fp+fn != 0):
        scor['accuracy'] = (tp+tn)/float(tp+tn+fp+fn)
    else:
        scor['accuracy'] = (tp+tn)/float(total_len)
    stpfp = 0;
    stpfn = 0;
    
    if(tp+fp == 0):
        scor['precision'] = 0;
    else:
        scor['precision'] = (tp)/float(tp+fp)
    
    if((tp+fn) == 0):
        scor['recall'] = 0;
    else:
        scor['recall'] = (tp)/float(tp+fn)
        
    scor['tp'] = tp
    scor['tn'] = tn
    scor['fp'] = fp
    scor['fn'] = fn
    scor['th1'] = thresh
    scor['th2'] = hthresh
    if(scor['precision']+scor['recall'] == 0):
        scor['F1'] = 0
    else:
        scor['F1'] = (2*scor['precision']*scor['recall'])/(scor['precision']+scor['recall'])    
    return scor;

import types
import pandas as pd
# from botocore.client import Config
# import ibm_boto3
import numpy as np

import multiprocessing
import os
import pandas as pd
import time
import pickle

def display_max_results(dfframe,framename):
    dfframe = dfframe[dfframe.recall != 1]
    newdata = pd.DataFrame()
    newdata = newdata.append(dfframe.loc[dfframe['accuracy'].idxmax()])
    newdata = newdata.append(dfframe.loc[dfframe['F1'].idxmax()])
    newdata['Max Value'] = ['Accuracy','F1']
    cols = newdata.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    newdata = newdata[cols]
    newdata.index.name = framename
    return newdata;

def display_frame(dfframe_p_causal,framename):
    dfframe_p_causal.index.name = framename
    return dfframe_p_causal

#@function bulk scoring + calculation of all metrics + multiprocessing + vectorization to make things even faster
def phrase_scorer(ce_data,score_thrs,hit_thresh,index,typecall='word',calctype='non-strict'):
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    print('Process ',os.getpid(),' started!')
    # ret_frame_causal = pd.DataFrame();
    ret_frame_standard = pd.DataFrame();
    l = 0;
    tot = float(len(score_thrs)*len(hit_thresh))
    ten = int(0.1*tot);
    
    cepairs = [];
    labels = np.array([c[2] for c in ce_data])
    if(typecall!='word'):
        cepairs,cepairs2 = get_chunks_batch(ce_data)
    else:
        cepairs = [[[c[0]],[c[1]]] for c in ce_data];
        cepairs2 = [[[c[1]],[c[0]]] for c in ce_data]
        
    fhitsli,rhitsli,chitsli = [[],[],[]]
    fres = do_query_block(es, index, cepairs,calltype='evidence')
    rres = do_query_block(es, index, cepairs2,calltype='evidence')
    # cres = do_query_block(es, index, cepairs,calltype='co_occurance')
    # print('obtained the query blocks')
    try:
        fhitsli = np.array([r['hits']['total'] for r in fres['responses']],float);
        rhitsli = np.array([r['hits']['total'] for r in rres['responses']],float);
        # chitsli = np.array([r['hits']['total'] for r in cres['responses']],float);
    except:
        print(fhitsli,rhitsli)
        exit(1)
        # pdb.set_trace()

    inli = [fhitsli,rhitsli,chitsli]    
    for ht in hit_thresh:
        for i,sc in enumerate(score_thrs):
            
            # scor_data1 = score_bulker(inli,labels,sc,ht,'causal',calctype)
            # ret_frame_causal = ret_frame_causal.append(pd.DataFrame(scor_data1,index=[l]))

            scor_data2 = score_bulker(inli,labels,sc,ht,'non_causal',calctype)
            ret_frame_standard = ret_frame_standard.append(pd.DataFrame(scor_data2,index=[l]))
            
            l+=1;
            # print(l)
            if(l%ten == 0):
                print(os.getppid(),'_PPID_',os.getpid(),'_PID_ ',(l/tot)*100,'% done!')
    print('Process ',os.getpid(),' ended!')
    ret_tup = (0,ret_frame_standard);
    # ret_tup = (ret_frame_causal,ret_frame_standard);
    return ret_tup;

def phrase_scorer_non_bulk(ce_data,score_thrs,hit_thresh,index,name,typecall='word',calctype='non-strict'):
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    print('Process ',os.getpid(),' started!')
    # ret_frame_causal = pd.DataFrame();
    ret_frame_standard = pd.DataFrame();
    l = 0;
    tot = float(len(score_thrs)*len(hit_thresh))
    ten = int(0.1*tot);
    
    cepairs = [];
    labels = np.array([c[2] for c in ce_data])
    
    import pickle

    if (os.path.isfile('results/'+name+'_'+index+typecall+'.pkl')):
        with open('results/'+name+'_'+index+typecall+'.pkl','rb') as rb:
            inli = pickle.load(rb)
    else:
        inli = modify_to_get_feq(es,ce_data,index,'phrase')
        with open('results/'+name+'_'+index+typecall+'.pkl','wb') as pkl:
            pickle.dump(inli,pkl)

    for ht in hit_thresh:
        for i,sc in enumerate(score_thrs):
            
            scor_data2 = score_bulker(inli,labels,sc,ht,'non_causal',calctype)
            ret_frame_standard = ret_frame_standard.append(pd.DataFrame(scor_data2,index=[l]))
            
            l+=1;
            # print(l)
            if(l%ten == 0):
                print(os.getppid(),'_PPID_',os.getpid(),'_PID_ ',(l/tot)*100,'% done!')
    print('Process ',os.getpid(),' ended!')
    ret_tup = (0,ret_frame_standard);
    # ret_tup = (ret_frame_causal,ret_frame_standard);
    return ret_tup;


def phrase_scorer_w(ce_data,score,iname,typecall='word',optn = 'causal'):
    print('Process ',os.getpid(),' started!')
    te,scor_data = scoring_phrases(ce_data,iname,score,typecall,optn)
    print('Process ',os.getpid(),' ended!')
    return scor_data;


"""
Allows to create children of child processes, something not possible by default in python's multiprocessing class 
"""
class nodaepross(multiprocessing.Process):
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class outer_pool(multiprocessing.pool.Pool):
    Process = nodaepross
