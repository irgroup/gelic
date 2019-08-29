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

####################################################################
# Configuration block 
####################################################################
run = "title_txt_de"
topicFiles = ["dnb-collection/dnb_topics.xml"]
solrBase = "http://localhost:8983/solr/"
solrInstance = "dnb_base"
params = ['indent=on', 'wt=json', 'fl=score,id', 'rows=1000']
solrParams = '&'.join(params)
field1 = "title_txt_de"
field2 = ""
field3 = ""

####################################################################
# Don't change things behind this line (except you know what to do).
####################################################################
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

        solrURL = solrBase+solrInstance+"/select?"+solrParams+"&q="+fieldQuery
        print("Querying " + topicId + " at " + solrURL)
        
        response = urllib.request.urlopen(solrURL)
        data = json.loads(response.read().decode('utf-8'))
        #print json.dumps(data)
        for i,d in enumerate(data['response']['docs']):
            line = ' '.join([topicId, '0', str(d['id']), str(i), str(d['score']), str(run), str('\n')])
            #print line
            f.write(line)

# close up the runFile
f.close()        
        
    


