# How to interpret the resulting files when running a script
## erschliessung.py (at this time only available in German, translation will follow)
CSV-Names: “topic1.csv” - “topic50.csv” + “erschliessung.csv”

Zunächst wird für jedes Topic eine CSV-Datei erstellt: also topic1.csv - topic50.csv.
In diesen CSVs wurden für das jeweilige topic alle DNB-IDs aus assessments.csv rausgezogen. Diese ID steht in der ersten Spalte. 
In der zweiten Spalte “topicid” steht die topicID, die der Nummer entspricht welche im Dateinamen steht. 
In der dritten Spalte “rel” steht die Relevanz für die DNB-ID der Spalte für das Topic, also 0-2. 
In der darauf folgenden Spalte 4 “subject_gnd” wird mit “y” gekennzeichnet, ob das Dokument intellektuell erschlossen ist. Wenn es nicht erschlossen ist, ist das Feld leer. Dies gilt auch für Spalte 5 und 6. 5 kennzeichnet eine Erschliessung durch den Verlag und die 6. durch die maschinelle Erschließung.
Diese Topic-Dateien werden in erschliessung.py zusammengefasst. In der ersten Spalte “topic” steht die topicID bzw. Nummer des Dateinamens. 
Die zweite Spalte “relevantGesamt” zeigt, wie viele Dokumente in der Testkollektion insgesamt als relevant bewertet wurden (also 1+2 zusammen).
In der dritten Spalte “relBeidseitig” wurde errechnet, wie viele von den relevanten Dokumenten doppelt erschlossen sind - also intellektuell UND maschinell/automatisch. In der vierten Spalte “relNurAuto” ist die Summe aller Dokumente die NICHT intellektuell, sondern NUR maschinell/automatisch und evt. vom Verlag erschlossen sind. In der fünften Spalte “relNurInt” stehen dazu gegensätzlich alle Dokumente der relevanten Dokumente, die NICHT maschinell, sondern NUR intellektuell un evt. vom Verlag erschlossen wurden. 
“relVLB” Spalte 6 ist die Summe aller relevanten Dokumente, die vom Verlag erschlossen wurden. Darunter können Dokumente sein, die doppelt intell. und masch. erschlossen wurden, oder die weder noch oder nicht doppelt erschlossen wurden.
Wenn also “relBeidseitig”, “relNurAuto” und “relNurInt” zusammengerechnet werden, entspricht die Summe nicht unbedingt “relevantGesamt”. Es gibt Dokumente die weder intellektuell, noch maschinell erschlossen wurden, aber trotzdem als relevant gewertet wurden. 
Wenn stattdessen “relBeidseitig”, “relNurAuto”, “relNurInt” UND “relNichtAutoNichtInt” summiert werden, ergibt sich “relevantGesamt”.

## evalpertopic.py
CSV-Names: "tE_PerTopic[...]_txt_de.csv", ...

The title of the .csv files consists of "tE_PerTopic" to mark which script was used and the fields which were searched e.g. "title_txt_de" and "vlb_txt_de separated with dashes: "tE_PerTopicTitle_txt_de-Vlb_txt_de.csv

1. Column : "topicId" : consists the topic Id-number
2. Column : "topicTitle" : name of the topic
3. Column : "num_ret" : total number of documents
4. Column : "num_rel" : total number of relevant documents
5. Column : "num_rel_ret" : number of found relevant documents
6. Column : recall
7. Column : precision 
8. Column : fmeasure

## evalsummary.py
CSV-Name: "tE_summary.csv"

1. Column : “field” : Lists all fields (separated by dashes) that are searched in Solr, e.g. in row “Gnd_txt_de-Auto_txt_de” the fields gnd_txt_de an auto_txt_de were searched.
2. Column : “num_ret” : Sum of how many documents were found across all topics when the fields in “field” where searched.
3. Column : “num_rel” : Sum of all documents that were relevant FOR the search in ALL topics that were queried. For some topics solr couldn’t find anything and these topics are excluded in trec_eval’s calculations. That’s why the number varies so much.
4. Column : “num_rel_ret” : Of “num_rel” where n documents retrieved. Of “num_ret” where n documents relevant.
5. Column : recall
6. Column : precision
7. Column : fmeasure

## synonyms.py
File-Name: synonyms.txt

synonym-1,synonym-2, … => preferred term

e.g.: Landwirtschaftschemie,Agrochemie,Agrarchemie => Agrikulturchemie
