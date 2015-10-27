import requests
import json
import csv

# This assumes that you have a csv with only one column containing names for person agents
# This will require some additional logic if some of the names have been parsed into "Primary Part of Name" and "Rest of Name" or
# if you also want to include corporate entities and family names
# It also sets the source for everything to 'local'. If you've done some reconciliation and have a source and authority id, those will also need to be added/modified

aspace_url = 'http://localhost:8089'
respository = '2'
username = 'admin'
password = 'admin'
resource_id = '1'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session':session}

# Grab the resource record json
resource = requests.get(aspace_url + '/repositories/' + repository+ '/resources/' + resource_id, headers=headers).json()

# Go through the csv of names and post them to ArchivesSpace
uris = []
with open(input_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row. Remove this line if your csv doesn't have headers
    next(reader,None)
    for row in reader:

        # The name is in the first column
        name = row[0]

        # Build the agent json
        # You may want to modify 'source', add an 'authority_id', include both 'primary_name' and 'rest_of_name', etc.
        agent_json = {'names':[{'primary_name':name,'name_order':'inverted','sort_name_auto_generate':True,'source':'local'}]}

        # Post the agent
        agent_post = requests.post(aspace_url+'/agents/people',headers=headers,data=json.dumps(agent_json)).json()

        # See if ArchivesSpace returned the URI for an existing record or a new URI for that name
        if 'error' in agent_post:
            uri = agent_post['error']['conflicting_record'][0]
            print "Agent record for {0} already exists: {1}".format(name,uri)
        else:
            uri = agent_post['uri']
            print "Created agent record for {0}: {1}".format(name,uri)

        # Add the agent URI to the list of URIs
        uris.append(uri)

# Loop through the list of URIs and add them as linked agents to the resource
for uri in uris:
    linked_agent = {'ref':uri,'role':'subject'}
    resource['linked_agents'].append(linked_agent)

# Post the updated resource
update_resource = requests.post(aspace_url+'/repositories/' + repositories + '/resources/' + resource_id,headers=headers,data=json.dumps(resource)).json()
