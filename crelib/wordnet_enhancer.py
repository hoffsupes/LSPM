
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################


"""
@Wordnet enhancement utility files
"""

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import genesis
import numpy as np
from scoring_utils import form_evidence_query,pross_ce_phrase

"""
Get synonyms from wordnet
"""
def get_synonyms(term,topn=10,thold=0.7):
    l = [];
    scores = [];
    scores2 = []
    li = wn.synsets(term)
    for ss in li:
        for s in ss.lemma_names():
            if '_' in s:
                tm = s.split('_');
                for t in tm:
                    l.append(t);
                    scores.append(ss.wup_similarity(li[0],simulate_root=True))
            l.append(s);
            scores.append(ss.wup_similarity(li[0],simulate_root=True))
    
    scores = np.array(scores);
    scores[scores == None]= 0
    scores = scores[scores > thold]
    return np.array(l)[np.argsort(scores)[::-1][:topn]].tolist()

"""
Enrich using the synonyms from wordnet
"""
def enrich_through_wordnet(ce,topn=10,thresh=0.8):
    ce1 = get_synonyms(ce[0][0],topn,thresh);
    ce2 = get_synonyms(ce[0][1],topn,thresh);
    return [ce1,ce2]

"""
Enrich using wordnet for whole phrases instead of single words
"""
def pross_phrase_wordnet(ce_phrase,topn=10,thresh=0.7):
    
    cause_cand, effect_cand = pross_ce_phrase(ce_phrase[0][0],ce_phrase[0][1])
    cause_pool = []
    effect_pool = []
#     print(ce_phrase)
#     print(cause_cand,effect_cand)
    for cause in cause_cand:
        cause_pool += get_synonyms(cause,topn,thresh);
    
    cause_pool += cause_cand;
    
    for effect in effect_cand:
        effect_pool += get_synonyms(effect,topn,thresh);
    
    effect_pool += effect_cand;
    
    return [cause_pool,effect_pool]

"""
@utility function: A quick way to get sense of accuracy when trying out the wordnet method (get accuracy metrics)
"""
def get_true_false_now(ce_sem,given_index_name,ll,uu,tp,fp,tn,fn,ctt,thresh,ccnet=2):
    from config import es
    label = ce_sem[ll:uu][0][2];
#     cepairs,cepairs2,cc1,cc2 = enrich_through_conceptnet(ce_sem[ll:uu],'word',ccnet)
    cepairs = enrich_through_wordnet(ce_sem[ll:uu],10,0)
    cc1 = ce_sem[ll:uu][0][0]
    cc2 = ce_sem[ll:uu][0][1]
    fr1,fr2,fre1,fre2 = [0,0,0,0]
    
#     ce2 = cepairs2
    ce1 = cepairs
    fr1 = form_evidence_query(es,given_index_name, [cc1]+ce1[0], [cc2]+ce1[1])['total']
    fr2 = form_evidence_query(es,given_index_name, [cc2]+ce1[1], [cc1]+ce1[0])['total']
    if(fr1):
        ctt+=1

    if(fr1):
        score = ((fr1+1.0)/(fr2+1.0))
    else:
        score = 0

    if float(score) >= thresh:
        if label.strip(' ').lower() == 'causal':
            tp+=1
        else:
            fp+=1;
    else:
        if label.strip(' ').lower() == 'non_causal':
            tn+=1;
        else:
            fn+=1;
    return tp,fp,tn,fn,ctt;

"""
@utility function: A quick way to get sense of accuracy when trying out the wordnet method (get accuracy metrics from a given benchmark)
"""

def do_word_processing_wordnet(ce_sem,given_index_name,threshame,name):
    fin = []
    for thresh in threshame:
        skipped = 0;
        tp,fp,tn,fn = [0,0,0,0];
        ctt = 0
        skipped_rows = []
        causal_skipped = 0;
        non_causal_skipped = 0;
        tt = {};
        tt['acc_measures'] = [];
        total = len(ce_sem)
        N = int(0.1*total);
        for i,c in enumerate(ce_sem):
            try:
                tp,fp,tn,fn,ctt = get_true_false_now(ce_sem,given_index_name,i,i+1,tp,fp,tn,fn,ctt,thresh,0)
            except Exception as E:
                skipped+=1;
                print(c,' skipped!',E)
                if(c[2].strip(' ') == 'causal'):
                    causal_skipped+=1;
                else:
                    non_causal_skipped+=1;
                skipped_rows.append(c)
            if(i%N == 0):
                print(((i*1.0)/total)*100,' done')
        tt['acc_measures'].append([tp,fp,tn,fn])
        tt['accuracy'] = ((tp+(1.0*tn))/(tp+fp+tn+(fn*1.0)));
        tt['recall'] = (((1.0*tp))/(tp+(fn*1.0)))
        tt['precision'] = (((1.0*tp))/(tp+(fp*1.0)))
        tt['F1'] = 2*(tt['precision']*tt['recall'])/(tt['precision']+tt['recall'])
        tt['skipped'] = skipped;
        tt['times_helped'] = ctt
        tt['causal_skipped'] = causal_skipped;
        tt['non_causal_skipped'] = non_causal_skipped;
        tt['skipped_rows'] = skipped_rows
        # print(tt)
        fin.append(tt)
    print(fin)
    import pickle
    with open('results/'+name+'_results_wordnet.pkl','wb') as wbb:
        pickle.dump(fin,wbb)

"""
@utility function: A quick way to get sense of accuracy when trying out the wordnet method (get accuracy metrics from a given benchmark) for phrases
"""

def get_true_false_phrase(ce_nato,given_index_name,ll,uu,tp,fp,tn,fn,ctt,thresh,ccnet=2,thold=0.7):
    from config import es
    label = ce_nato[ll:uu][0][2];
#     cepairs,cepairs2,cc1,cc2 = enrich_through_conceptnet(ce_nato[ll:uu],'word',ccnet)
#     cepairs = enrich_through_wordnet(ce_nato[ll:uu],10,0.00001)
    cepairs = pross_phrase_wordnet(ce_nato[ll:uu],10,thold)
    
    fr1,fr2,fre1,fre2 = [0,0,0,0]
    
#     ce2 = cepairs2
    ce1 = cepairs
    fr1 = form_evidence_query(es, given_index_name, ce1[0], ce1[1])['total']
    fr2 = form_evidence_query(es, given_index_name, ce1[1], ce1[0])['total']
    
    if(fr1):
#         print('fre1',fr1)
#         print('fre2',fr2)
        ctt+=1

#     fr2 = do_query_block(es, 'cause_effect_init_new1', ce2,calltype='evidence')
    if(fr1):
        score = ((fr1+1.0)/(fr2+1.0))
    else:
        score = 0
#     print('Score:',score)
#     print('score,fr1,fr2,fre1,fre2',score,fr1,fr2,fre1,fre2)
    if float(score) >= thresh:
        if label.strip(' ').lower() == 'causal':
            tp+=1
        else:
            fp+=1;
    else:
        if label.strip(' ').lower() == 'non_causal':
            tn+=1;
        else:
            fn+=1;
    return tp,fp,tn,fn,ctt;

"""
Use wordnet for phrase based benchmarks
"""
def do_phrase_processing_wordnet(ce_risk,given_index_name,threshrange,name):
    fin = []
    for thold in [0]:
        for thresh in threshrange:
        #     T = [];
            skipped = 0;
            tp,fp,tn,fn = [0,0,0,0];
            ctt = 0
            skipped_rows = []
            causal_skipped = 0;
            non_causal_skipped = 0;
            tt = {};
            tt['acc_measures'] = [];
            total = len(ce_risk)
            N = int(0.1*total);
            for i,c in enumerate(ce_risk):
                try:
                    tp,fp,tn,fn,ctt = get_true_false_phrase(ce_risk,given_index_name,i,i+1,tp,fp,tn,fn,ctt,thresh,1.0,thold)
                except Exception as E:
                    skipped+=1;
                    print(c,' skipped!',E)
                    if(c[2].strip(' ') == 'causal'):
                        causal_skipped+=1;
                    else:
                        non_causal_skipped+=1;
                    skipped_rows.append(c)
                # print(ctt,' instances where it helped so far out of ',i, ' sentences')    
                # print(tp,fp,tn,fn,'accuracy',((tp+(1.0*tn))/(tp+fp+tn+(fn*1.0))))
                # T.append([tp,fp,tn,fn])
                if(i%N == 0):
                    print(((i*1.0)/total)*100,' done')
            tt['acc_measures'].append([tp,fp,tn,fn])
            tt['accuracy'] = ((tp+(1.0*tn))/(tp+fp+tn+(fn*1.0)));
            if(not(tp == 0 and fn == 0)):
                tt['recall'] = (((1.0*tp))/(tp+(fn*1.0)))
            else:
                tt['recall'] = 0
            if(not(fp == 0 and tp == 0)):
                tt['precision'] = (((1.0*tp))/(tp+(fp*1.0)))
            else:
                tt['precision'] = 0;
            if(not(tt['precision'] == 0 and tt['recall'] == 0)):
                tt['F1'] = 2*(tt['precision']*tt['recall'])/(tt['precision']+tt['recall'])
            else:
                tt['F1'] = 0
            tt['skipped'] = skipped;
            tt['times_helped'] = ctt
            tt['causal_skipped'] = causal_skipped;
            tt['non_causal_skipped'] = non_causal_skipped;
            tt['skipped_rows'] = skipped_rows
            tt['similarity_thold'] = thold
            tt['causal_threshold'] = thresh
            print(tt)
            fin.append(tt)
    print(fin)
    import pickle
    with open('results/'+name+'_results_wordnet.pkl','wb') as wbb:
        pickle.dump(fin,wbb)

def main():
    import pandas as pd

    projdir = 'benchmarks'

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

    # do_word_processing_wordnet(ce_sem,'100_million_index_creator_new_index_corpus_new_1',[1.5,0.6],'Semeval_100_mil_large');
    # print('done with semeval')
    # do_phrase_processing_wordnet(ce_risk,'100_million_index_creator_new_index_corpus_new_1',[0.5,0.1],'Risk_100_mil_large');
    # print('done with Risk')
    do_phrase_processing_wordnet(ce_nato,'100_million_index_creator_new_index_corpus_new_1',[0.8,0.3],'NatoSFA_100_mil_large');
    print('done with NatoSFA')
    do_phrase_processing_wordnet(ce_me,'100_million_index_creator_new_index_corpus_new_1',[1,0.4],'ME_100_mil_large');
    print('done with ME')

if __name__ == '__main__':
    main()