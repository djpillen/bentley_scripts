"""
curl -H "X-ArchivesSpace-Session:$TOKEN" -d '{"source":"lcsh","vocabulary":"/vocabularies/1","terms":[{"term":"Cheese", "term_type":"topical","vocabulary":"/vocabularies/1"},{"term":"Michigan","term_type":"geographic","vocabulary":"/vocabularies/1"}]}' http://localhost:8089/subjects
"""

import requests
import json
import csv
import time
from datetime import datetime

start_time = datetime.now()

subjects_csv = 'C:/Users/Public/Documents/aspace_subjects.csv'

baseURL = 'http://localhost:8089'
user='admin'
password='admin'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

'''
enum_sources = []
ead_sources = []
update_enum = 0

with open(subjects_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        source = row[1]
        if source not in ead_sources:
            ead_sources.append(source)

enumerations = requests.get(baseURL+'/config/enumerations', headers=headers).json()

for enumeration in enumerations:
    if enumeration['name'] == 'subject_source':
        source_uri = enumeration['uri']

subject_sources = requests.get(baseURL+source_uri,headers=headers).json()

for value in subject_sources['enumeration_values']:
    enum_sources.append(value['value'])

for source in ead_sources:
    if source not in enum_sources:
        new_source = {"value":source,"suppressed":False,"jsonmodel_type":"enumeration_value"}
        subject_sources['enumeration_values'].append(new_source)
        update_enum += 1

if update_enum > 0:
    subject_sources_json = json.dumps(subject_sources)
    update_sources = requests.post(baseURL+source_uri, data=subject_sources_json, headers=headers).json()
    print update_sources
'''

'''
subject_ids = requests.get(baseURL+'/subjects?all_ids=true').json()

for i in subject_ids:
    subject_json = requests.get(baseURL+'/subjects/'+str(i)).json()
    print subject_json['title'], subject_json['uri']
'''


with open(subjects_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row_indexes = len(row) - 1
        source = row[1]
        terms_list = []
        for row_num in range(3,row_indexes + 1, 2):
            term = row[row_num]
            term_type = row[row_num+1]
            terms_dict = {}
            terms_dict["term"] = term
            terms_dict["term_type"] = term_type
            terms_dict["vocabulary"] = "/vocabularies/1"
            terms_list.append(terms_dict)

        data = json.dumps({"source":source,"vocabulary":"/vocabularies/1","terms":[i for i in terms_list]})
        subjects = requests.post(baseURL+'/subjects', headers=headers, data=data).json()
        if 'status' in subjects:
            if subjects['status'] == 'Created':
                subject_uri = subjects['uri']
                row.append(subject_uri)
                with open('C:/Users/Public/Documents/posted_subjects.csv','ab') as csv_out:
                    writer = csv.writer(csv_out)
                    writer.writerow(row)
        print subjects

end_time = datetime.now()

print "Script start time:", start_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script end time:", end_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script running time:", end_time - start_time
