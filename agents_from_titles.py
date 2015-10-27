import requests
import json
import csv
import re

aspace_url = 'http://141.211.39.87:8089'
username = 'admin'
password = 'admin'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session':session}

resource_id = '1864'


def find_titles(child,titles):
    title = child['title']
    titles.append(title)
    if child['has_children']:
        for child in child['children']:
            find_titles(child,titles)
    return titles


resource = requests.get(aspace_url+'/repositories/2/resources/' + resource_id, headers=headers).json()
resource_tree = requests.get(aspace_url+'/repositories/2/resources/' + resource_id +'/tree', headers=headers).json()

with open('C:/Users/Public/Documents/agents_from_titles.json','w') as json_out:
    json_out.write(json.dumps(resource, indent=4))

with open('C:/Users/Public/Documents/agents_from_titles_tree.json','w') as json_out:
    json_out.write(json.dumps(resource_tree,indent=4))

for child in resource_tree['children']:
    titles = find_titles(child,titles=[])

with open('C:/Users/Public/Documents/titles_csv.txt','a') as csvfile:
    #writer = csv.writer(csvfile)
    for title in titles:
        title = re.sub(r'<(.*?)>','',title)
        csvfile.write(title + '\n')
