"""
curl -H "X-ArchivesSpace-Session:$TOKEN" -d '{"source":"lcsh","vocabulary":"/vocabularies/1","terms":[{"term":"Cheese", "term_type":"topical","vocabulary":"/vocabularies/1"},{"term":"Michigan","term_type":"geographic","vocabulary":"/vocabularies/1"}]}' http://localhost:8089/subjects
"""

import requests
import json
import csv


baseURL = 'http://localhost:8089'
user='admin'
password='admin'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

"""
subject_ids = requests.get(baseURL+'/subjects?all_ids=true').json()

for i in subject_ids:
    subject_json = requests.get(baseURL+'/subjects/'+str(i)).json()
    print subject_json['title'], subject_json['uri']
"""

with open('post_subjects.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        terms_list = []
        for i in range(0,10):
            try:
                term, term_type = row[i].split(':')
                terms_dict = {}
                terms_dict["term"] = term
                terms_dict["term_type"] = term_type
                terms_dict["vocabulary"] = "/vocabularies/1"
                terms_list.append(terms_dict)
            except StandardError:
                continue
        data = json.dumps({"source":"lcsh","vocabulary":"/vocabularies/1","terms":[i for i in terms_list]})
        subjects = requests.post(baseURL+'/subjects', headers=headers, data=data).json()
        print subjects
