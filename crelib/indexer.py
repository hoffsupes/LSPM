
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

"""

Indexing utility functions
Used in a variety of places within this whole codebase

"""
import sys
from itertools import (takewhile,repeat)
from multiprocessing import Pool
import gc
import re
import os
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
    from causal_identification import get_all_cause_effects
    import parameter_config
    from parameter_config import time,create_new_index
else:
    from .causal_identification import get_all_cause_effects
    from . import parameter_config
    from .parameter_config import time,create_new_index

"""
global parameter for control over batch size while indexing and stoppage criterion
"""
maxSents = -1
sentChunkNumber = 2000;

"""
Index a cause effect pair
"""
def push_to_network_li(cause,effect,sentenceli,index_name,doctype):
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    rret = [];
    # print('in push to network!')
    if(not(es.indices.exists(index=index_name))):
        print("Index not found! Please create an index with response = es.indices.create(index='"+index_name+"'')")
        return 0;
    res = es.search(        index=index_name,        body=        {           "query": {             "bool": {               "must": [                 { "match_phrase": { "cause": cause.lower() } },                 { "match_phrase": { "effect": effect.lower() } }               ]             }           }        }    )
#     print(res)
    if(res['hits']['total']):
        b1 = {    "cause": cause.lower(),    "effect": effect.lower(),    "count": res['hits']['hits'][0]['_source']['count'] + 1,    "evidences": res['hits']['hits'][0]['_source']['evidences'] + [s.lower() for s in sentenceli]    };
        updb1 = {"doc":b1}
        rret = es.update(index=index_name,body=updb1,id=res['hits']['hits'][0]['_id'])  
    else:
        b2 = {"cause":cause.lower(),    "effect": effect.lower(),    "count":1,    "evidences":[s.lower() for s in sentenceli]    };
        rret = es.index(index=index_name,body=b2)
    return rret

"""
Trying to index a cause effect pair trystopper times
"""
def persistent_indexing(cause,effect,sentenceli,index_name,doctype):
    # print('indexing ',cause,' ',effect)
    tryvar = 1;
    while(tryvar<=parameter_config.trystopper):
        try:
            ret = push_to_network_li(cause,effect,sentenceli,index_name,doctype)
            if('result' not in ret.keys()):
                print('retrying, will try for ',parameter_config.trystopper-tryvar,' times')
                time.sleep(tryvar*0.1)
                tryvar+=1;
                continue;
            elif(not(ret['result'] == 'created') and not(ret['result']=='updated')):
                print('retrying, will try for ',parameter_config.trystopper-tryvar,' times')
                time.sleep(tryvar*0.1)
                tryvar+=1;
                continue;
            break;             
        except Exception as E:
            tryvar+=1;
            print('retrying, will try for ',parameter_config.trystopper-tryvar,' times')
            time.sleep(tryvar*0.1)
    if(tryvar > parameter_config.trystopper):
        print('Failed to index ',cause,' and ',effect);
        return 0;
    return 1;

"""
Network creation functions for later versions
"""

def process_network(dat_iter,islog='A'): ### Dat_iter is a FILE pointer
    t0 = time.time();
    Cue_Found = None
    i_start = 0
    i_end = 0
    i_count = 0;
    caus_s = 0
    idxcounter = 10;
    if(islog == 1):
        filename = os.path.basename(dat_iter.name)
        filename[:filename.find('.txt')]
        logw = open(filename+'_log_.txt','a+');

    while (i_end != maxSents):
        t1 = time.time();
        sentLst = list()
        print("Processing batch "+str(i_count)+" of sentences of size: ",sentChunkNumber)
        print("Total Sentences Processed:",i_start," Causal Sentences so far:",caus_s)

        if(islog == 1):
            if(i_count%idxcounter == 0):
                logw.write(filename+" ---> Sentences processed: "+str(i_start)+"\n")

        for i,line in enumerate(dat_iter):      ### dat_iter is the file pointer here, IMPORTANT if not file pointer then this will not work
            if(len(line) == 0):
                continue;
            if(type(line) == type([])):
                sent = line[0].strip().replace('\n',"")
            elif type(line) == type(''):
                sent = line.strip().replace('\n',"")
            else:
                continue;
            if(len(sent) == 0 or re.search('[a-zA-Z0-9]',sent) == None):
                continue;
            sentLst.append(sent)
            if (i+1) == sentChunkNumber or (i_start + i+1== maxSents):
                break
        if (len(sentLst) == 0):
            break
        i_end += len(sentLst)
        dict_caus = get_all_cause_effects(sentLst);
        
        for keys in dict_caus.keys():
            persistent_indexing(dict_caus[keys]['cause'],dict_caus[keys]['effect'],dict_caus[keys]['evidences'],parameter_config.index_name,parameter_config.doctype)
            # elasti_net(dict_caus,keys,parameter_config.index_name,parameter_config.doctype)
#             persistent_indexing(dict_caus[keys]['cause'],dict_caus[keys]['effect'],dict_caus[keys]['evidences'],parameter_config.index_name,parameter_config.doctype)
            caus_s+=1
        # print(len(list(dict_caus.keys())))
        # print(dict_caus)    
        i_count+=1;
        t2 = time.time()
        print("Total time elapsed: ",t2-t0," seconds")
        print("Total taken to process this batch: ",t2-t1," seconds")
        i_start = i_end;
        del sentLst;
        del dict_caus;
    if(islog == 1):
        logw.close();
    print('Done!')

"""
To chunk an iterator / list into chunks of size n
"""
def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

"""
To chunk an iterator / list into chunks of size n with when total size cannot be obtained from the iterator
"""
def chunker_tot(seq, size,total_s):
    return (seq[pos:pos + size] for pos in range(0, total_s, size))

###########################################
##### Mini network creation for local runs
def run_multi(dat_iter,len_dat_iter,segments=8):
    chunks = chunker_tot(dat_iter, int(len_dat_iter / segments))
    poolputs = zip(chunks)
    try:
        pool2 = Pool(segments)
        retval = pool2.starmap(process_network, poolputs)
    except Exception as E:
        print('Error in mid pool',E)
    finally: 
        pool2.close()
        pool2.join() #### Correct this

"""
To count the number of lines in a file the fastest way possible
"""
def rawincount(filename):           ## Count the number of lines in a very large text file very fast!
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen )

"""
To run a single threaded version for network creation which goes from sentence level to index creation
"""
def run_data_single(filepath,islog='A'):
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    print(create_new_index(es,parameter_config.index_name))
    with open(filepath,'r') as filew:
        process_network(filew,islog)

"""
A single threaded version which does indexing in batches
"""
def index_corpus(dat_iter,corpus_index,batch_size = 10000,corpus_size=25000000):
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    from elasticsearch import helpers
    import string
    print(create_new_index(es,corpus_index))
    A = [];
    for i,sent in enumerate(dat_iter):      ### dat_iter is the file pointer here, IMPORTANT if not file pointer then this will not work
        sent = sent.strip().replace('\n',"")
        newsent = sent.lower().translate(str.maketrans('', '', string.punctuation))
        dat = {'headline':newsent}
        A.append({'_op_type':'index','_type':'headlines','_index':corpus_index,'_source':dat})
        if(i%batch_size == 0):
            res = helpers.bulk(es, A)
            A = []
            print((i/corpus_size*1.0)*100,'% done for process ',os.getpid())
    if(len(A)):
        res = helpers.bulk(es, A)



"""
The number of cause effect pairs within the network
"""
def display_network_count(index_name):
    parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
    if __name__ == '__main__' or parent_module.__name__ == '__main__':
        from config import es
    else:
        from .config import es
    res = es.search(index=index_name, body = {
    'size' : 10000,
    'query': {'match_all':{}}})
    print('Total network size:',res['hits']['total'])


"""
main()
"""
def main():
    import sys
    fil = sys.argv[1]
    parameter_config.index_name = sys.argv[2]
    run_data_single(fil,1)

if __name__ == '__main__':
    main()
