
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################


"""
Binary causal question answering module

Parameters described:

given_index_name: Index name over which it performs the binary causal question answering. If not given uses default value (cause_effect_testing_pipeline_dev)

@example cli usage:

python3 crelib bcqa

"""

import sys
from os import system
parent_module = sys.modules['.'.join(__name__.split('.')[:-1]) or '__main__']
if __name__ == '__main__' or parent_module.__name__ == '__main__':
	import parameter_config
else:
	from . import parameter_config

"""
Do binary causal question answering
"""
def bcqa(given_index_name):
	if __name__ == '__main__' or parent_module.__name__ == '__main__':
		from config import es
		from scoring_utils import form_evidence_query
	else:
		from .config import es
		from .scoring_utils import form_evidence_query
	cont = 'yes'

	while(cont.lower() != 'no'):
		system('clear')
		cause = input("\nEnter a cause: ").strip(' ').strip()
		effect = input("\nEnter it's supposed effect: ").strip(' ').strip()
		fhits = form_evidence_query(es,given_index_name,[cause],[effect])['total']
		rhits = form_evidence_query(es,given_index_name,[effect],[cause])['total']

		score = 0;
		ans = 'No'
		if(fhits):
			score = (fhits + 1.0) / (rhits + 1.0)

		if(score >= 1):
			ans = 'Yes'

		print('\n\nCould ',cause, ' cause ',effect,'?')
		print('\nAnswer:',ans,' with confidence ',score)
		cont = input("\n Continue? (Enter 'yes' or 'y' to continue and 'no' to stop) ").strip(' ').strip()

def main():
	try:
		given_index_name = sys.argv[1]
	except:
		given_index_name = parameter_config.index_name
	bcqa(given_index_name)

if __name__ == '__main__':
	main()