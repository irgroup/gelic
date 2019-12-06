#!/usr/local/bin/python3

# importing the needed libs
import csv, json, re, pandas as pd

# opening the json file and loading the data of the file to the variable "data"
dnbFile = 'authorities-sachbegriff_lds_20190613.jsonld'
with open(dnbFile, "r") as datafile:
    data = json.load(datafile)

# regex to later sort out ids that are not needed (!= ids from preferredName-Synonyms)
aboutregex = re.compile(r"(about)")
# regex to get the id from the dnb-link
idregex = re.compile('(http:\/\/d\-nb\.info\/gnd\/)(.*)')

synonyms = []

for listofdicts in data:
    
    for itemdicts in listofdicts:
        idList = []
        
        for k, v in itemdicts.items():
            
            if k == '@id':
                if aboutregex.findall(v):
                    continue
                elif idregex.findall(v):
                    match = idregex.search(v)
                    identifier = match.group(2)
                    ## FOR CSV-FILE
                    #idList.append(identifier)
                    
            if k == 'http://d-nb.info/standards/elementset/gnd#variantNameForTheSubjectHeading':
                for synonymdict in v:
                    for k, v in synonymdict.items():
                        synonym = v
                    idList.append(',' + synonym)
            
            if k == 'http://d-nb.info/standards/elementset/gnd#preferredNameForTheSubjectHeading':
                for preferreddict in v:
                    for k, v in preferreddict.items():
                        preferredname = v
                        idList.append(' => ' + preferredname)  
        
        synonyms.append(idList)
        idList = idList.sort(reverse=True)
        #print(idList)

synonyms = [i for i in synonyms if i]

## CSV-FILE
#syndf = pd.DataFrame(synonyms)
#syndf.to_csv('synonyms.csv', sep=',', index=False, header=False)

## SOLR-SYNONYM-FORMAT TXTFILE
with open('synonyms.txt', 'w', encoding='utf8') as resultFile: 
    for line in synonyms:
        word = ''.join(line)
        word = word.strip(',')
        if word.startswith(' =>'):
            continue
        else:
            resultFile.write(word + '\n')