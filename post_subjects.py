import csv
from datetime import datetime
import json
import requests
import time


start_time = datetime.now()

subjects_csv = 'C:/Users/djpillen/GitHub/test_run/subjects/aspace_subjects.csv'
posted_csv = 'C:/Users/djpillen/GitHub/test_run/subjects/posted_subjects.csv'

baseURL = 'http://141.211.39.87:8089'
user='admin'
password='admin'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}


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
                with open(posted_csv,'ab') as csv_out:
                    writer = csv.writer(csv_out)
                    writer.writerow(row)
        print subjects

end_time = datetime.now()

print "Script start time:", start_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script end time:", end_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script running time:", end_time - start_time
