
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################


"""
Get effects given a cause

"""

import sys
from os import system
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	import parameter_config
else:
	from . import parameter_config

def get_effects(es,cause,index_name):
	res = es.search(
        index= index_name,
        body=
        {
          "query": {
            "match_phrase": {
              "cause": cause
            }
          }
        }
    )
	effects = [r['_source']['effect'] for r in res['hits']['hits']]
	return effects;

"""
Do effect mining
"""
def emining(given_index_name):
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
	else:
		from .config import es
	cont = 'yes'

	while(cont.lower() != 'no'):
		system('clear')
		cause = input("\nEnter a cause: ").strip(' ').strip()
		effects = get_effects(es,cause,given_index_name)
		print('\n',cause,' causes:\n')
		for effect in effects:
			print(effect)
		print('\n')
		cont = input("\n Continue? (Enter 'no' to stop) ").strip(' ').strip()

def main():
	try:
		given_index_name = sys.argv[1]
	except:
		given_index_name = parameter_config.index_name
	emining(given_index_name)

if __name__ == '__main__':
	main()
