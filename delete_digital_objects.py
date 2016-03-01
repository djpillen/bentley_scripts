import requests
import json

auth = requests.post('http://localhost:8089/users/admin/login?password=admin').json()
session = auth['session']
headers = {"X-ArchivesSpace-Session":session}

digital_objects = requests.get('http://localhost:8089/repositories/2/digital_objects?all_ids=true',headers=headers).json()

for digital_object in digital_objects:
	delete_object = requests.delete('http://localhost:8089/repositories/2/digital_objects/'+str(digital_object),headers=headers).json()
	print delete_object