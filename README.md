
# LSPM

Large Scale Pattern Mining / Large Scale Causal Relation Extraction

Takes any corpus / text file with sentences in every line and extracts causal sentences and cause and effects from them. Also creates a network from the same and is able to perform the task of binary causal question answering from it.

## Installation  

- [Make sure you have python3 installed](https://realpython.com/courses/installing-python-windows-macos-linux/)
- Clone this repo or download it as a zip file
- Unzip it and traverse into the root of this repository
- Open a terminal and execute the following:
    - `python3 crelib/setup_script.py`
    - `python3 -c 'import nltk; nltk.download('popular')`
- input your credentials into the config.py in the crelib folder

## Usage

Important: Please note that all paths given below are not relative but absolute (full) paths. The corpus you give as input should be a text file where each line is a sentence. For outputs you get the causal sentences in a similar fashion (in a line by line fashion) but you get the cause-effect pairs in form of a jsonl file. Although you can directly use the name of the file directly (if it is present within the same directory from where you're calling these modules from as seen in the examples below) it is highly reccomended that you use full paths. Please use python instead of python3 if that's how your setup is.

### Test script

To run all of the modules below in one go, please open a terminal and traverse to the root of the directory and then execute:

```
chmod +x test_script.sh
./test_script.sh
```

OR

```
make run-tests
```

### Sentence Ingester Module 

(Please skip if you've already **preprocessed** your sentences)

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib ingest /full/path/to/input_text_corpus /full/path/to/cleaned_corpus_text_file
```

eg.

```
# ingest data
python3 crelib ingest input_test_data.txt cleaned_test_file.txt
```
### Causal Sentence Identification Module

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib causalsent /full/path/to/cleaned_corpus_text_file /full/path/to/causal_sentences_text_file
```

eg.

```
# ingest data
python3 crelib ingest input_test_data.txt cleaned_test_file.txt;
# get causal sentences
python3 crelib causalsent cleaned_test_file.txt causal.txt
```

### Cause-Effect Extraction Module

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib causeeffect /full/path/to/causal_sentences_text_file /full/path/to/cause_effect_json_file
```

eg.

```
# ingest data
python3 crelib ingest input_test_data.txt cleaned_test_file.txt;
# get causal sentences
python3 crelib causalsent cleaned_test_file.txt causal.txt;
# get cause effect pairs
python3 crelib causeeffect causal.txt cause_effects.jsonl
```
### Cause-Effect Indexing Module

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib index /full/path/to/input_cause_effect_json_file optional_value_index_name optional_value_doctype
```

eg.

```
# ingest data
python3 crelib ingest input_test_data.txt cleaned_test_file.txt;
# get causal sentences
python3 crelib causalsent cleaned_test_file.txt causal.txt;
# get cause effect pairs
python3 crelib causeeffect causal.txt cause_effects.jsonl
# index cause effect pairs
python3 crelib index cause_effects.jsonl
```

The `index_name` and `doctype` parameters are optional and if not given, default values for them will be used (`cause_effect_testing_pipeline_dev` and `cause_effect_pairs` respectively). If the index does not exist it will be created.

### Benchmark Scoring module

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib scoring /full/path/to/benchmarks_folder optional_index_name 
```

eg.

```
# do scoring
python3 crelib scoring benchmarks
```

The `index_name` is optional and if not given, default values for it will be used (`cause_effect_testing_pipeline_dev`). The benchmarks folder must be the benchmark folder included in this repository.

### Binary Causal Question Answering Module

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib bcqa optional_index_name 
```

eg.

```
# do bcqa
python3 crelib bcqa
```

Follow the instructions on screen as the program runs. The `index_name` is optional and if not given, default values for it will be used (`cause_effect_testing_pipeline_dev`). The benchmarks folder must be the benchmark folder included in this repository.

### Single Threaded Single Node Standalone End to End Pipeline Module

Open a terminal and traverse to the root of the codebase / repository and execute:

```
python3 crelib pipeline /full/path/to/input_text_corpus /full/path/to/cleaned_corpus_text_file /full/path/to/causal_sentences_text_file /full/path/to/cause_effect_json_file /full/path/to/benchmarks_folder optional_value_index_name optional_value_doctype
```

eg.

```
# complete pipeline run
python3 crelib pipeline input_test_data.txt cleaned_pipeline_test_file.txt causal_pipeline.txt cause_effects_pipeline.jsonl benchmarks
```

The index_name and doctype parameters are optional and if not given, default values for them will be used (`cause_effect_testing_pipeline_dev` and `cause_effect_pairs respectively`). If the index does not exist it will be created.

### Makefile tests

If you want to test individual modules described above with a single commmand, there's separate functionality for that. Open a terminal and traverse to the root directory of the repository and execute: 

#### For testing all modules

```
make run-tests
```

#### For testing the ingestion module

```
make ingest-test
```

#### For testing the causal sentence module

```
make causal-sent-test
```

#### For testing the cause effect module

```
make cause-effect-test
```

#### For testing the indexing module

```
make index-test
```

## Library use in your own program

The library is available for use in your own python program as:

```
import crelib
```

Further usage can be done as:

```
import crelib
crelib.setup_script.do_setup_libraries(1); ## Will install all the required libraries
```

## Requirements

The following libraries are required for running the code

- nltk
- elastisearch
- pyspark
- pandas
- psutil
- python3

## Expected Warnings

     RequestError(400, 'resource_already_exists_exception', 'index [index_name/----] already exists')
This is an expected message meaning that the index already exists. The system always tries to automatically create an index when it is given it's name and if it exists it simply continues as normal.

The elasticsearch indices used in the past towards this project might not exist anymore (they were attached to a cluster within the IBM cloud by default). Hence indexing might noe work as expected (especially any default examples) but the rest of the modeules, including causal sentence identification, cause effect extraction and others would do fine. 
