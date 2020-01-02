
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

## EDS connection imports
from elasticsearch import Elasticsearch
from ssl import create_default_context
# @hidden_cell

# The following code sets up connection to elasticsearch service.
context = create_default_context(
   cadata = "-----BEGIN CERTIFICATE-----\n"+
            "-----END CERTIFICATE-----")
es = Elasticsearch(

)
