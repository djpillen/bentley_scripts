import requests
import json

#Change these
aspace_url = 'http://localhost:8089'
username = 'admin'
password = 'admin'

auth = requests.post("{0}/users/{1}/login?password={2}".format(aspace_url, username, password)).json()
session = auth['session']
headers = {"X-ArchivesSpace-Session":session}

agent_types = ["people", "corporate_entities", "families"]

for agent_type in agent_types:

	agent_ids = ["3386"] #requests.get("{0}/agents/{1}?all_ids=true".format(aspace_url, agent_type),headers=headers).json()
	total = len(agent_ids)
	count = 1
	for agent_id in agent_ids:
		print "Publishing {0} that are linked to published records - {1}/{2}".format(agent_type, count, total)
		agent = requests.get("{0}/agents/{1}/{2}".format(aspace_url, agent_type, agent_id),headers=headers).json()
		if agent['is_linked_to_published_record'] and not agent['publish']:
			agent['publish'] = True
			response = requests.post("{0}/agents/{1}/{2}".format(aspace_url, agent_type, agent_id),headers=headers, data=json.dumps(agent)).json()
			print response
		count += 1