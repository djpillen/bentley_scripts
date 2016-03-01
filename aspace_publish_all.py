import requests
import json
import getpass

aspace_url = 'http://localhost:8089'
username = 'admin'
password = getpass.getpass('Password:')

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session':session}

with requests.Session() as s:
    resources = s.get(aspace_url+'/repositories/2/resources?all_ids=true',headers=headers).json()
    digital_objects = s.get(aspace_url+'/repositories/2/digital_objects?all_ids=true',headers=headers).json()

for resource in resources:
    publish = requests.post(aspace_url+'/repositories/2/resources/'+str(resource)+'/publish',headers=headers).json()
    print publish

for digital_object in digital_objects:
    publish = requests.post(aspace_url+'/repositories/2/digital_objects/'+str(digital_object)+'/publish',headers=headers).json()
    print publish
