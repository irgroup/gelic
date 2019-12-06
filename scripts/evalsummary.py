#!/usr/local/bin/python3
# Small script to search a local solr instance with differnt queries 
# @author: Philipp Schaer
# @email: philipp.schaer@th-koeln.de

####################################################################
# Imports
####################################################################

import csv
import json
import os
import pandas as pd
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

####################################################################
# Configuration block 
####################################################################

run = "title_txt_de"
topicFiles = ["components/topics.xml"]
solrBase = "http://localhost:8983/solr/"
solrInstance = "gelic"
params = ['indent=on', 'wt=json', 'fl=score,id', 'rows=1000']
solrParams = '&'.join(params)
trecEvalValues = ['num_ret','num_rel','num_rel_ret']

####################################################################
# Don't change things behind this line (except you know what to do).
####################################################################

with open("scripts/fieldnames.json", "r") as datafile:
    data = json.load(datafile)

# variable for trec_eval-run throughs
v = 1
numOfValues = len(trecEvalValues)

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
            topicId = topic.find('identifier').text
            fieldQuery = field1+":("+str(urllib.parse.quote(query))+")"
            if field2:
                fieldQuery = fieldQuery + "%20OR%20" + field2 + ":("+str(urllib.parse.quote(query))+")"
            if field3:
                fieldQuery = fieldQuery + "%20OR%20" + field3 + ":("+str(urllib.parse.quote(query))+")"
            if field4:
                fieldQuery = fieldQuery + "%20OR%20" + field4 + ":("+str(urllib.parse.quote(query))+")"

            solrURL = solrBase+solrInstance+"/select?"+solrParams+"&q="+fieldQuery
            #print("Querying " + topicId + " at " + solrURL)

            response = urllib.request.urlopen(solrURL)
            data = json.loads(response.read().decode('utf-8'))
            #print json.dumps(data)
            for i,d in enumerate(data['response']['docs']):
                line = ' '.join([topicId, '0', str(d['id']), str(i), str(d['score']), str(run), str('\n')])
                f.write(line)
    
    # closing opened files 
    f.close() 

    # regexing up the 'fieldnames' so they can be used later on
    field1 = field1.upper()
    field2 = field2.upper()
    field3 = field3.upper()
    field4 = field4.upper()
    
    regex = re.compile(r"(SUBJECT_|)(.*)(_TXT_DE|_SS)")
    
    field1 = regex.search(field1)
    if field1:
        field1 = str(field1.group(2)).capitalize() + str(field1.group(3)).capitalize()
    else:
        field1 = ''
    field2 = regex.search(field2)
    if field2:
        field2 = '-' + str(field2.group(2)).capitalize() + str(field2.group(3)).capitalize()
    else:
        field2 = ''
    field3 = regex.search(field3)
    if field3:
        field3 = '-' + str(field3.group(2)).capitalize() + str(field3.group(3)).capitalize()
    else:
        field3 = ''
    field4 = regex.search(field4)
    if field4:
        field4 = '-' + str(field4.group(2)).capitalize() + str(field4.group(3)).capitalize()
    else:
        field4 = ''

    valueNumber = 1

    for value in trecEvalValues:
        # getting the trec_eval results for each wanted value
        os.system("trec_eval/trec_eval -m " + str(value) + " components/assessments.txt title_txt_de.txt > su" + str(value) + ".csv")
        
        with open("su2" + str(value) + ".csv", "w") as resultFile:
            # writing the header
            resultFile.write('field' + ';' + str(value) + '\n')
            
            with open("su" + str(value) + ".csv", "r") as inputFile:
                
                for line in inputFile:
                    # cleaning the file up to have a consistent divider
                    cleaning = line.replace('\t', ';')
                    cleaning2 = cleaning.replace(' ', '')
                    # splitting the columns
                    col = cleaning2.split(';')
                    # writing fieldname + col1 to the resultFile
                    resultFile.write(str(field1) + str(field2) + str(field3) + str(field4) + ';' + str(col[2]))
                    
        # importing all the csv.-files of the different values to pandas 
        vars()['data' + str(valueNumber + 1)] = pd.read_csv("su2" + str(value) + ".csv", sep=';')
        
        valueNumber = valueNumber + 1
    
    frames = []
    # appending data to frames list
    for num in range(1,numOfValues+1):
       frames.append(vars()['data' + str(num+1)])
    # concatinating frames
    result = pd.concat(frames, axis=1)
    # removing duplicate columns
    result = result.loc[:,~result.columns.duplicated()]    
    result.to_csv('su3' + str(field1) + str(field2) + str(field3) + str(field4) + '.csv', sep=';', index=False, decimal=',')
    
    v = v + 1 

csvNumber = 1
for csvFilename in os.listdir('.'):
    if csvFilename.startswith('su3'):
        #print(csvFilename)
        vars()['csv' + str(csvNumber + 1)] = pd.read_csv(csvFilename, sep=';')
        csvNumber = csvNumber+1
    else:
        continue 

dframes = []
# appending data to dframes list
for num in range(1,csvNumber):
   dframes.append(vars()['csv' + str(num+1)])
# concatinating frames
result = pd.concat(dframes, axis=0)

# removing duplicate columns
result = result.loc[:,~result.columns.duplicated()]

# calculating unranked values
result['recall'] = (result['num_rel_ret']/result['num_rel']).round(decimals=2)
result['precision'] = (result['num_rel_ret']/result['num_ret']).round(decimals=2)
result['fmeasure'] = ((2*result['precision']*result['recall'])/(result['precision']+result['recall'])).round(decimals=2)

# saving result to tE_summary.csv  
result.to_csv('tE_summary.csv', sep=';', index=False, decimal=',')

# removing unneeded files
for csvFilename in os.listdir('.'):
    if csvFilename.startswith('su'):
        os.remove(csvFilename)
    else:
        continue 
os.remove('title_txt_de.txt')

print("Finished!")