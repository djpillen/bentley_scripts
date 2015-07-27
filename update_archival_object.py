import requests
import json
import csv

'''
curl -H "X-ArchivesSpace-Session:$TOKEN" 'http://localhost:8089/repositories/2/search?page=1&q='2668ec2a1d88a5cabcf9db744d446059''
'''

aspace_url = 'http://localhost:8089'
username= 'admin'
password = 'admin'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

with open('C:/Users/Public/Documents/7.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        identifier = row[3]
        ref_id = row[2]
        search = requests.get(aspace_url+'/repositories/2/search?page=1&q='+ref_id,headers=headers).json()
        archival_object_uri = search['results'][0]['uri']
        archival_object_json = requests.get(aspace_url+archival_object_uri,headers=headers).json()
        if archival_object_json['ref_id'] == ref_id:
            print 'match!'
        row.append(archival_object_uri)
        display_string = archival_object_json['display_string']

        dig_obj = {'title':display_string,'digital_object_id':identifier}

        dig_obj_data = json.dumps(dig_obj)

        dig_obj_post = requests.post(aspace_url+'/repositories/2/digital_objects',headers=headers,data=dig_obj_data).json()

        print 'Digital Object Status', dig_obj_post['status']

        dig_obj_uri = dig_obj_post['uri']

        print 'Digital Object URI', dig_obj_uri

        row.append(dig_obj_uri)

        dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}

        archival_object_json['instances'].append(dig_obj_instance)

        archival_object_data = json.dumps(archival_object_json)

        archival_object_update = requests.post(aspace_url+archival_object_uri,headers=headers,data=archival_object_data).json()

        print archival_object_update

        with open('C:/Users/Public/Documents/7_temp.csv','ab') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)
