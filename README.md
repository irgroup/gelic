# GeLIC - German Library Indexing Collection

*Gelic is Proto-Germanic for "like, alike, similar" (see [Wiktionary](https://en.wiktionary.org/wiki/gelic)).* 

This repository contains the following items:

- `gelic_components` contains the documents, relevance assessments and topics
    - `gelic_assessments.txt` contains relevance assessments
    - `gelic_collection` contains the title data of the documents
    - `gelic_topics.xml` contains topics used for evaluation
- `src` contains a bunch of conversion and analysis scripts
- `gelic_eval-scripts` contains trec_eval-like scripts to evaluate different search settings with gelic
    - `search.py` is a script to search a local solr instance with different queries. The results of the queries are then evaluated by trec_eval and the evaluations are saved as a csv-file
    - `fieldnames.json`contains the different variations of "fields to search in" for search.py

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
