run-tests:
	chmod +x test_script.sh
	./test_script.sh

ingest-test:
	echo "ingest-test started"
	python3 crelib ingest input_test_data.txt cleaned_test_file.txt;
	echo "ingest-test done!"

causal-sent-test:
	echo "causal sentence test started"
	python3 crelib ingest input_test_data.txt clean_test_file.txt;
	python3 crelib causalsent clean_test_file.txt causal_1.txt;
	echo "causal sentence test done!"

cause-effect-test:
	echo "cause effect test started"
	python3 crelib ingest input_test_data.txt clean_test_file_2.txt;
	python3 crelib causalsent clean_test_file_2.txt causal_2.txt;	
	python3 crelib causeeffect causal_2.txt cause_effects_2.jsonl
	echo "cause effect test ended!" 

index-test:
	echo "indexing test started"
	python3 crelib ingest input_test_data.txt clean_test_file_3.txt;
	python3 crelib causalsent clean_test_file_3.txt causal_3.txt;
	python3 crelib causeeffect causal_3.txt cause_effects_3.jsonl;
	python3 crelib index cause_effects_3.jsonl;
	echo "indexing test ended"

scoring-test:
	echo "scoring test started"
	python3 crelib scoring benchmarks
	python3 crelib bcqa
	echo "scoring test ended"