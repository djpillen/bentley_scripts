import requests
import json
import csv
import re

# Given an ArchivesSpace resource id, this will grab the tree for that resource and
# output the titles of all children archival objects to a csv for clean up, named entity
# recognition, and reconciliation using your favorite method for doing those things

output_csv = '/path/to/output.csv'

aspace_url = 'http://localhost:8089'
repository = '2'
username = 'admin'
password = 'admin'
resource_id = '1'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth['session']
headers = {'X-ArchivesSpace-Session':session}

# Fetch the resource tree
resource_tree = requests.get(aspace_url+'/repositories/' + repository + '/resources/' + resource_id +'/tree', headers=headers).json()

# Function to loop through all children in the resource tree and grab the title
def find_titles(child,titles):
    title = child['title']
    titles.append(title)
    if child['has_children']:
        for child in child['children']:
            find_titles(child,titles)
    return titles

all_titles = []
# Loop through all the children in the resource tree (presumably series, subgroups, etc) and pass them to the find_titles function
for child in resource_tree['children']:
    all_titles.extend(find_titles(child,titles=[]))



# Write the titles to a csv
with open(output_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    for title in all_titles:
        title = re.sub(r'<(.*?)>','',title)
        writer.writerow([title.strip()])

# Then, do the clean up, parsing, NER, reconciliation, etc. and send that result to post_agents_from_titles.py
