import requests
import json

auth = requests.post('http://localhost:8089/users/admin/login?password=admin').json()
session = auth['session']
headers = {"X-ArchivesSpace-Session":session}

resources = requests.get('http://localhost:8089/repositories/2/resources?all_ids=true',headers=headers).json()

for resource in resources:
	delete_object = requests.delete('http://localhost:8089/repositories/2/resources/'+str(resource),headers=headers).json()
	print delete_object