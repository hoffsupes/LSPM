
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""
Utility functions for performing causal sentence identification and cause effect extraction
"""

import re
import sys
import os
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    import parameter_config
else:
    from . import parameter_config


#################################################################################################################################################
### Various preprocessing functions for cleaning cause effect pairs

SEP = '###'

cause_drop_re = re.compile('(^why )|(^how )|( may$)|( will$)|( could$)|( can$)|( likely$)|( helped$)|( a$)|( would$)|( to$)|(\?)', re.IGNORECASE)
effect_drop_re = re.compile('(^to a)|(^to)|(^of)', re.IGNORECASE)
effect_remove_re = re.compile('(^from )|(^by )', re.IGNORECASE)

def remove_source(str):
    i = str.rfind("-")
    if i > 0:
        str = str[:i]
    i = str.rfind("|")
    if i > 0:
        str = str[:i]
    str = str.replace("`","").replace("‘","").replace("’","").replace("'","").replace('"','').strip()
    return str

def fix_cause(cause):
    cause = cause_drop_re.sub('', cause).strip()
    cause = remove_source(cause)
    cause = cause.replace(SEP," ")
    return cause

def fix_effect(effect):
    effect = effect_drop_re.sub('', effect).strip()
    if (len(effect_remove_re.findall(effect))>0):
        return ""
    effect = remove_source(effect)
    effect = effect.replace(SEP, " ")
    return effect

###
#################################################################################################################################################

"""
Get causal sentences only from a list of sentences
"""
def get_causal_sentences_only(init_list):
    result = [];
    r_result = [];
    
    result += [k for k in init_list for tt in parameter_config.verbs if(len(re.findall('\\b'+tt+'\\b',k)))]
    r_result += [k for k in init_list for tt in parameter_config.reverse_verbs if(len(re.findall('\\b'+tt+'\\b',k)))]

    return result + r_result;

"""
Get causal sentences only from a list of sentences in form of an iterator
"""
def get_causal_sentences_only_iter(init_list):
    return iter(get_causal_sentences_only(init_list));

def get_causal_sentences_only_lse(init_list):
    result = [];
    r_result = [];
    
    result += [k for k in init_list for tt in parameter_config.verbs if tt in k]
    r_result += [k for k in init_list for tt in parameter_config.reverse_verbs if tt in k]

    return result + r_result;

"""
The user provides their own custom verb list dynamically, can be useful in cases when the user needs to perform some kind of specialized detection
"""
def get_all_cause_effects_custom_list(init_list,forward_verbs,backward_verbs):
    evidences = {}
    result = [];
    r_result = [];
    
    result += [k for k in init_list for tt in forward_verbs if(len(re.findall('\\b'+tt+'\\b',k)))]
    r_result += [k for k in init_list for tt in backward_verbs if(len(re.findall('\\b'+tt+'\\b',k)))]
        
    for verb in forward_verbs:
        for title in [r for r in result if(len(re.findall('\\b'+verb+'\\b',r)))]:
            parts = title.split(verb)
            if len(parts) == 2:
                cause = fix_cause(parts[0].strip())
                effect = fix_effect(parts[1].strip())
                if cause == '' or effect == '':
                    continue
                cestr = cause + SEP + effect
                if cestr not in evidences:
                    evidences[cestr] = {"cause":cause, "effect":effect,"evidences":[title]};
                    continue;
                evidences[cestr]["evidences"] += [title];
    for verb in backward_verbs:
        for title in [r for r in r_result if(len(re.findall('\\b'+verb+'\\b',r)))]:
            parts = title.split(verb)
            if len(parts) == 2:
                effect = fix_effect(parts[0].strip())
                cause = fix_cause(parts[1].strip())
                if cause == '' or effect == '':
                    continue
                cestr = cause + SEP + effect
                if cestr not in evidences:
                    evidences[cestr] = {"cause":cause, "effect":effect,"evidences":[title]};
                    continue;
                evidences[cestr]["evidences"] += [title];        
    return evidences

"""
Get all cause effects and causal sentences given a list of sentences
"""
def get_all_cause_effects(init_list):
    evidences = {}
    result = [];
    r_result = [];
    
    result += [k for k in init_list for tt in parameter_config.verbs if(len(re.findall('\\b'+tt+'\\b',k)))]
    r_result += [k for k in init_list for tt in parameter_config.reverse_verbs if(len(re.findall('\\b'+tt+'\\b',k)))]
        
    for verb in parameter_config.verbs:
        for title in [r for r in result if(len(re.findall('\\b'+verb+'\\b',r)))]:
            parts = title.split(verb)
            if len(parts) == 2:
                cause = fix_cause(parts[0].strip())
                effect = fix_effect(parts[1].strip())
                if cause == '' or effect == '':
                    continue
                cestr = cause + SEP + effect
                if cestr not in evidences:
                    evidences[cestr] = {"cause":cause, "effect":effect,"evidences":[title]};
                    continue;
                evidences[cestr]["evidences"] += [title];
    for verb in parameter_config.reverse_verbs:
        for title in [r for r in r_result if(len(re.findall('\\b'+verb+'\\b',r)))]:
            parts = title.split(verb)
            if len(parts) == 2:
                effect = fix_effect(parts[0].strip())
                cause = fix_cause(parts[1].strip())
                if cause == '' or effect == '':
                    continue
                cestr = cause + SEP + effect
                if cestr not in evidences:
                    evidences[cestr] = {"cause":cause, "effect":effect,"evidences":[title]};
                    continue;
                evidences[cestr]["evidences"] += [title];        
    return evidences

"""
Alternate function which one can optionally use if needed, does a "loose" search instead of a strict term based search if so is ever needed
"""
def get_all_cause_effects_loose(init_list):
    evidences = {}
    result = [];
    r_result = [];
    
    result += [k for k in init_list for tt in parameter_config.verbs if tt in k]
    r_result += [k for k in init_list for tt in parameter_config.reverse_verbs if tt in k]
        
    for verb in parameter_config.verbs:
        for title in [r for r in result if(verb in r)]:
            parts = title.split(verb)
            if len(parts) == 2:
                cause = fix_cause(parts[0].strip())
                effect = fix_effect(parts[1].strip())
            #   print("Cause: %s - Effect: %s" % (cause,effect))
                if cause == '' or effect == '':
                    continue
                cestr = cause + SEP + effect
                if cestr not in evidences:
                    evidences[cestr] = {"cause":cause, "effect":effect,"evidences":[title]};
                    continue;
                evidences[cestr]["evidences"] += [title];
    for verb in parameter_config.reverse_verbs:
        for title in [r for r in r_result if(verb in r)]:
            parts = title.split(verb)
            if len(parts) == 2:
                effect = fix_effect(parts[0].strip())
                cause = fix_cause(parts[1].strip())
                if cause == '' or effect == '':
                    continue
                cestr = cause + SEP + effect
                if cestr not in evidences:
                    evidences[cestr] = {"cause":cause, "effect":effect,"evidences":[title]};
                    continue;
                evidences[cestr]["evidences"] += [title];        
    return evidences

"""

This is an alternate function (for performing cause-effect extraction and causal sentence identification and then writing results directly then and there) which you can use if you wanted.

"""
def cre(sentence,mode='process',csenpath=None,ceffpath=None):
    if(mode == 'write'):
        csen = open(csenpath,'a+');
        ceff = open(ceffpath,'a+')
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    if(debug_mode):
        print('indexed sentence:',sentence);
    def push_to_network_lcre(cause,effect,sentenceli,index_name,doctype):
        rret = [];
        if(not(es.indices.exists(index=index_name))):
            print("Index not found! Please create an index with response = es.indices.create(index='"+index_name+"'')")
            return 0;
        res = es.search(        index= index_name,        body=        {           "query": {             "bool": {               "must": [                 { "match_phrase": { "cause": cause.lower() } },                 { "match_phrase": { "effect": effect.lower() } }               ]             }           }        }    )
        if(res['hits']['total']):
            b1 = {    "cause": cause.lower(),    "effect": effect.lower(),    "count": res['hits']['hits'][0]['_source']['count'] + 1,    "evidences": res['hits']['hits'][0]['_source']['evidences'] + [s.lower() for s in sentenceli]    };
            updb1 = {"doc":b1}
            rret = es.update(index=index_name,body=updb1,id=res['hits']['hits'][0]['_id'])  
        else:
            b2 = {"cause":cause.lower(),    "effect": effect.lower(),    "count":1,    "evidences":[s.lower() for s in sentenceli]    };
            rret = es.index(index=index_name,body=b2)
        return rret
    def persistent_indexingcre(cause,effect,sentenceli,index_name,doctype):
        tryvar = 1;
        while(tryvar<=trystopper):
            try:
                ret = push_to_network_lcre(cause,effect,sentenceli,index_name,doctype)
                if('result' not in ret.keys()):
                    print('retrying, will try for ',trystopper-tryvar,' times')
                    time.sleep(tryvar*0.1)
                    tryvar+=1;
                    continue;
                elif(not(ret['result'] == 'created') and not(ret['result']=='updated')):
                    print('retrying, will try for ',trystopper-tryvar,' times')
                    time.sleep(tryvar*0.1)
                    tryvar+=1;
                    continue;
                break;             
            except Exception as E:
                tryvar+=1;
                print('retrying, will try for ',trystopper-tryvar,' times')
                time.sleep(tryvar*0.1)
        if(tryvar > trystopper):
            print('Failed to index ',cause,' and ',effect);
            return 0;
        return 1;
    gc.collect();

    dict_caus = get_all_cause_effects([sentence]);
    tot_keys = len(dict_caus.keys())

    if(tot_keys):
        if(mode == 'write'):
            csen.write(sentence+'\n');
    for keys in dict_caus.keys():
        if(debug_mode):
            print('indexed cause effect:',dict_caus[keys]['cause'],dict_caus[keys]['effect']);
        if(mode == 'write'):
            ceff.write('Cause:'+dict_caus[keys]['cause']+', Effect:'+dict_caus[keys]['effect']+', Sentences:'+str(dict_caus[keys]['evidences'])+'\n')
        persistent_indexingcre(dict_caus[keys]['cause'],dict_caus[keys]['effect'],dict_caus[keys]['evidences'],index_name,doctype)
    if(mode == 'write'):
        ceff.close()
        csen.close()

    return 1;