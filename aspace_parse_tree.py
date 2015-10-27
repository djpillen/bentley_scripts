import json

filename = 'C:/Users/Public/Documents/agents_from_titles_tree.json'

resource_tree = json.loads(open(filename,'r').read())

def find_titles(child):
    title = child['title']
    print title
    if child['has_children']:
        for child in child['children']:
            find_titles(child,titles)
    return titles

for child in resource_tree['children']:
    find_titles(child)
