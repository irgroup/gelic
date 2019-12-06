# GeLIC - German Library Indexing Collection

*Gelic is Proto-Germanic for "like, alike, similar" (see [Wiktionary](https://en.wiktionary.org/wiki/gelic)).* 

This repository contains the following items:

- `components` contains the documents, relevance assessments and topics
    - `assessments.txt` contains relevance assessments
    - `corpus.zip` contains the title data of the documents
    - `topics.xml` contains topics used for evaluation
- `src` contains a bunch of conversion and analysis scripts
- `scripts` contains scripts to automizie different tasks that emerged in the course of the project 
    - `evalsummary.py` is a script to search a local solr instance with the titles of the topics.xml as queries. `fieldnames.json` specifies in which fields solr searches. Variations could be: 1. only in "subject_auto_txt_de" 2. only in "subject_gnd_txt_de" 3. "subject_auto_txt_de" and "subject_gnd_txt_de". The results of each fieldnames-variation of queries are then evaluated by trec_eval and summarized. Thus the script is most suitable if you want a quick comparision between variations of fields that are searched in. These summary-evaluations are then saved as a csv-file. 
    - `evalpertopic.py` automizes similar processes as `evalsummary.py` and only the endresult differs. Instead of writing a summary in a single csv-file, the script creates as many csv-files as there are variations in `fieldnames.json`. In these csv-files are the trec_eval result for each query of the variation e.g. a csv-file for the variation "subject_auto_txt_de" in which the recall, precision and f measure of topics like "Kritische Theorie" can be found.
	- `erschliessung.py` results in a list of all topics with counts regarding the occurences of relevant documents divided in machine content indexing, conventional content indexing etc.
    - `synonyms.py` extracts the gnd-synonyms and their preferred term from the jsonld-file `authorities-sachbegriff_lds_20190613.jsonld` and transforms the terms in a solr-readable synonyms.txt-file. Warning! Before using, follow the instructions of src/README.md Plus: if you want a .csv-list, there is also a commented out option in the script.

## Authors

This repository is joined work of the following people:

- Philipp Schaer ([phschaer](https://github.com/phschaer), project lead)
- Klaus Lepsky ([klepsky](https://github.com/klepsky), project lead)
- Ina Böckmann ([iboeckma](https://github.com/iboeckma))
- Sebastian Pommerencke ([SebastianPommerencke](https://github.com/SebastianPommerencke))
- Sven Gaida ([SvenGaida](https://github.com/SvenGaida))
- Felix van Tellingen ([fvantellingen](https://github.com/fvantellingen))

### Alumni

- Johanna Munkelt ([FH Dortmund](https://www.fh-dortmund.de/de/addresses/munkelt_johanna.php))
