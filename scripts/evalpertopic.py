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

# variable for csv-filenames of trec_eval run throughs
v = 1

for lines in data:
    # declaring field1-4
    field1 = lines['f1']
    field2 = lines['f2']
    field3 = lines['f3'] 
    field4 = lines['f4']

    # opening the file where all the topics with their ids are to be stored
    topics = open('pTtopics.csv', 'w')
    # writing the header
    topics.write('topicId' + ';' + 'topicTitle' + '\n')
    
    f = open(run+'.txt', 'w')

    for topicFile in topicFiles:
        # parse topicFile
        root = ET.parse(topicFile).getroot()    
        #print("Querying the topics at " + field1 + "via solr")
        for topic in root.findall('topic'):
            query = topic.find('title').text
            # query = query.replace(' ',' AND ')
            topicId = topic.find('identifier').text
            fieldQuery = field1+":("+str(urllib.parse.quote(query))+")"
            print(fieldQuery)
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
            
            for i,d in enumerate(data['response']['docs']):
                line = ' '.join([topicId, '0', str(d['id']), str(i), str(d['score']), str(run), str('\n')])
                f.write(line)
                #print(line)

            topicLine = str(topicId) + ';' + str(query) + '\n'
            topics.write(topicLine) 
    
    # closing opened files 
    f.close()
    topics.close()

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
        os.system("trec_eval/trec_eval -q -n -m " + str(value) + " components/assessments.txt title_txt_de.txt > pT" + str(value) + ".csv")
        
        with open("pT2" + str(value) + ".csv", "w") as resultFile:
            # writing the header
            resultFile.write('topicId' + ';' + str(value) + '\n')
            
            with open("pT" + str(value) + ".csv", "r") as inputFile:
                
                for line in inputFile:
                    # cleaning the file up to have a consistent divider
                    cleaning = line.replace('\t', ';')
                    cleaning2 = cleaning.replace(' ', '')
                    # splitting the columns
                    col = cleaning2.split(';')
                    # writing col 2 + 3 to the file
                    resultFile.write(str(col[1]) + ';' + str(col[2]))

        # importing all the csv.-files of the different values to pandas 
        vars()['data' + str(valueNumber + 1)] = pd.read_csv("pT2" + str(value) + ".csv", sep=';', dtype={'topicId' : 'Int64', str(value) : 'Int64'})
        
        valueNumber = valueNumber + 1

    # importing the pTtopics.csv to pandas / naming it 'merged1' so it can be used in the following loop
    merged1 = pd.read_csv("pTtopics.csv", sep=';', dtype={'topicId' : 'Int64', 'topicTitle' : 'str'})
    # counting the number of values for the merging process
    numOfValues = len(trecEvalValues)
    # merging the dataframes together
    for num in range(1,numOfValues+1):
        vars()['merged' + str(num + 1)] = pd.merge(vars()['merged' + str(num)], vars()['data' + str(num + 1)], how='outer', on='topicId')
    
    # calculating unranked values
    merged4['recall'] = (merged4['num_rel_ret']/merged4['num_rel']).round(decimals=2)
    merged4['precision'] = (merged4['num_rel_ret']/merged4['num_ret']).round(decimals=2)
    merged4['fmeasure'] = ((2*merged4['precision']*merged4['recall'])/(merged4['precision']+merged4['recall'])).round(decimals=2)
    
    # writing the resulting dataframe to csv-files
    merged4.to_csv('tE_PerTopic' + str(field1) + str(field2) + str(field3) + str(field4) + '.csv', sep=';', index=False, decimal=',')

    v = v + 1

# removing unneeded files
for csvFilename in os.listdir('.'):
    if csvFilename.startswith('pT'):
        os.remove(csvFilename)
    else:
        continue 
os.remove('title_txt_de.txt')

print("Finished!")