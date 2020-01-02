#!/bin/bash 
#
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################
#

# Test script for the LSPM project

echo "Testing individual components!"
python3 crelib ingest input_test_data.txt cleaned_test_file.txt;
python3 crelib causalsent cleaned_test_file.txt causal.txt;
python3 crelib causeeffect causal.txt cause_effects.jsonl
python3 crelib index cause_effects.jsonl
echo "Individual components done!"

echo "Testing pipeline!"
python3 crelib pipeline input_test_data.txt cleaned_pipeline_test_file.txt causal_pipeline.txt cause_effects_pipeline.jsonl benchmarks
echo "Pipeline tested!"