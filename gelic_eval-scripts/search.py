#!/usr/local/bin/python3
# Small script to search a local solr instance with differnt queries 
# @author: Philipp Schaer
# @email: philipp.schaer@th-koeln.de

####################################################################
# Imports
####################################################################
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import os
import pandas as pd
import csv

####################################################################
# Configuration block 
####################################################################
run = "title_txt_de"
topicFiles = ["dnb-collection/dnb_topics.xml"]
solrBase = "http://localhost:8983/solr/"
solrInstance = "dnb_base"
params = ['indent=on', 'wt=json', 'fl=score,id', 'rows=1000']
solrParams = '&'.join(params)

####################################################################
# Don't change things behind this line (except you know what to do).
####################################################################
with open("fieldnames.json", "r") as datafile:
    data = json.load(datafile)

# variable for csv-filenames of trec_eval-run throughs
v = 1

for lines in data:
    # declaring field1-4
    field1 = lines['f1']
    field2 = lines['f2']
    field3 = lines['f3'] 
    field4 = lines['f4']

    f = open(run+'.txt', 'w')

    for topicFile in topicFiles:
        # parse topicFile
        root = ET.parse(topicFile).getroot()    
        for topic in root.findall('topic'):
            query = topic.find('title').text
            # query = query.replace(' ',' AND ')
            topicId = topic.find('identifier').text
            fieldQuery = field1+":("+str(urllib.parse.quote(query))+")"
            if field2:
                fieldQuery = fieldQuery + "%20OR%20" + field2 + ":("+str(urllib.parse.quote(query))+")"
            if field3:
                fieldQuery = fieldQuery + "%20OR%20" + field3 + ":("+str(urllib.parse.quote(query))+")"
            if field4:
                fieldQuery = fieldQuery + "%20OR%20" + field4 + ":("+str(urllib.parse.quote(query))+")"

            solrURL = solrBase+solrInstance+"/select?"+solrParams+"&q="+fieldQuery
            print("Querying " + topicId + " at " + solrURL)

            response = urllib.request.urlopen(solrURL)
            data = json.loads(response.read().decode('utf-8'))
            #print json.dumps(data)
            for i,d in enumerate(data['response']['docs']):
                line = ' '.join([topicId, '0', str(d['id']), str(i), str(d['score']), str(run), str('\n')])
                # print line
                f.write(line)
    
    # close up the runFile 
    f.close() 

    os.system("trec_eval/trec_eval dnb-collection/dnb_rel.txt title_txt_de.txt > " + str(v) + ".csv")  
    print("Passing runFile of query " + str(v) + " to trec_eval and saving the data to " + str(v) + ".csv")
    v = v + 1 

# pandas can't merge the dataframes as long as one column is called "runid". 
# and because the runid-column can't be renamed with pandas,
# the file headers are changed in the following with the csv module
for csvFilename in os.listdir('.'):
    if not csvFilename.endswith('.csv'):
        continue    # skip non-csv files
    elif csvFilename.endswith('result.csv'):
        continue    # skip result-csv
    
    inputFileName = csvFilename
    outputFileName = os.path.splitext(inputFileName)[0] + "_modified.csv"

    with open(inputFileName, newline='') as inFile, open(outputFileName, 'w', newline='') as outfile:
        r = csv.reader(inFile)
        w = csv.writer(outfile)

        next(r, None)  # skipping old header
        # write new header
        w.writerow(['wert' + '\t' + 'all' + '\t' + 'ausgabe'])

        # copy the rest
        for row in r:
            w.writerow(row)


#ToDo: storing data1-8 in list -> iterate over items instead of vars()... ? (https://stackoverflow.com/questions/15161657/iteration-over-variable-names-in-python) 
for num in range(1,9):
    # reading 1-8.csvs to pandas, delimiter = tab
    vars()['data' + str(num)] = pd.read_csv(str(num) + "_modified.csv", sep='\t')
    # deleting 'all'-columns from dataframes 
    vars()['data' + str(num)].drop(columns="all", inplace=True)
    # stripping the wert column of white spaces
    vars()['data' + str(num)]['wert'] = vars()['data' + str(num)]['wert'].str.strip()

# renaming column 'title_text_de' to name which describes which fields are searched
data1.rename(columns={'ausgabe':'titleAndAuto'}, inplace=True)
data2.rename(columns={'ausgabe':'titleAutoAndVLB'}, inplace=True)
data3.rename(columns={'ausgabe':'titleAutoAndGND'}, inplace=True)
data4.rename(columns={'ausgabe':'titleAutoVLBAndGND'}, inplace=True)
data5.rename(columns={'ausgabe':'titleAndVLB'}, inplace=True)
data6.rename(columns={'ausgabe':'titleVLBAndGND'}, inplace=True)
data7.rename(columns={'ausgabe':'titleAndGND'}, inplace=True)
data8.rename(columns={'ausgabe':'title'}, inplace=True)

# "renaming" data1 so it can be used in the following loop
newdata1 = data1 
# merging the dataframes together
print("Merging trec_eval results...")
for num in range(1,8):
    vars()['newdata' + str(num + 1)] = pd.merge(vars()['newdata' + str(num)], vars()['data' + str(num + 1)], on='wert')
    #print("Merging dataframes of the " + str(num) + " and " + str(num +1) + " queries together.")

# writing the resulting dataframe to result.csv
newdata8.to_csv('result.csv', index=False)

#removing files that are not needed anymore
print("Removing unneeded files...")
for csvFilename in os.listdir('.'):
    if csvFilename.endswith('_modified.csv'):
        os.remove(csvFilename)
    else:
        continue 

for num in range(1,9):
    os.remove(str(num) + ".csv")

os.remove('title_txt_de.txt')

print("Finished!")