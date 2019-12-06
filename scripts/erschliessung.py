import csv, os, pandas as pd, xml.etree.ElementTree as ET

metadata = 'corpus.xml'
reldata = 'assessments.csv'
parsed = ET.parse(metadata)
root = parsed.getroot()

data1 = []
for doc in root:
    dnb = {}
    for field in doc.findall('field'):
        afield = field.attrib
        for k, v in afield.items():
            if v == 'id':
                #print(v, field.text)
                dnb['dnbid'] = field.text.lstrip("0")
            if v == 'subject_gnd_ss':
                dnb[v] = 'y'
            if v == 'subject_auto_ss':
                dnb[v] = 'y'
            if v == 'subject_vlb_ss':
                dnb[v] = 'y'

    data1.append(dnb)
df1 = pd.DataFrame(data1)
df1.to_csv('df1.csv', sep=';', index=False)

relevancelist = []
with open(reldata, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # skip first row
    next(csv_reader)
    for line in csv_file:
        col = line.replace('\n', '').split(';')
        rela = {}
        for x in col:
            rela['dnbid'] = col[1].lstrip("0")
            rela['topicid'] = col[0]
            rela['rel'] = col[2]
        relevancelist.append(rela)
df2 = pd.DataFrame(relevancelist)
df2.to_csv('df2.csv', sep=';', index=False)

merged = pd.merge(df2,df1) 
for num in range(1,51):
    topicfile = merged.loc[lambda merged: merged['topicid'] == str(num)]
    topicfile.to_csv('topic' + str(num) + '.csv', sep=';', index=False)


data3 = []
for csvFilename in os.listdir('.'):
    
    if csvFilename.startswith('topic'):
        
        with open (csvFilename, "r") as inputFile:
            rel = {'topic' : 0, 'relevantGesamt' : 0, 'relBeidseitig' : 0, 'relNurAuto' : 0, 'relNurInt' : 0, 'relVLB' : 0, 'relNichtAutoNichtInt' : 0}
            csv_reader = csv.reader(inputFile, delimiter=';')
            next(csv_reader)
            
            for line in csv_reader:
                rel['topic'] = line[1]
                
                if line[2] == '2':
                    rel['relevantGesamt'] = rel['relevantGesamt'] + 1
                    
                    if line[4] == 'y':
                        rel['relVLB'] = rel['relVLB'] + 1

                    if line[5] == 'y':
                        if line[3] == 'y':
                            rel['relBeidseitig'] = rel['relBeidseitig'] + 1
                        else: 
                            rel['relNurAuto'] = rel['relNurAuto'] + 1
                    elif line[3] == 'y':
                        rel['relNurInt'] = rel['relNurInt'] + 1
                    else: 
                        rel['relNichtAutoNichtInt'] = rel['relNichtAutoNichtInt'] + 1
                
                elif line[2] == '1':
                    rel['relevantGesamt'] = rel['relevantGesamt'] + 1
                    
                    if line[4] == 'y':
                        rel['relVLB'] = rel['relVLB'] + 1

                    if line[5] == 'y':
                        if line[3] == 'y':
                            rel['relBeidseitig'] = rel['relBeidseitig'] + 1
                        else: 
                            rel['relNurAuto'] = rel['relNurAuto'] + 1
                    elif line[3] == 'y':
                        rel['relNurInt'] = rel['relNurInt'] + 1
                    else: 
                        rel['relNichtAutoNichtInt'] = rel['relNichtAutoNichtInt'] + 1

            if rel['topic'] != 0:
                data3.append(rel)

df3 = pd.DataFrame(data3)
#print(df3)
df3.to_csv('erschliessung.csv', sep=';', index=False)

