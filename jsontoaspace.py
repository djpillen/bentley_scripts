import requests
import os
from os.path import join
import json

baseURL = 'http://localhost:8089'
repository = '2'
user = 'admin'
password = 'admin'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]

headers = {'Content-type': 'application/json', 'X-ArchivesSpace-Session': session}

path = 'test_json'
for filename in os.listdir(path):
    data = open(join(path, filename), 'rb')
    jsontoresource = requests.post(baseURL + '/repositories/2/batch_imports', headers=headers, data=data).json()
    for result in jsontoresource:
        if 'saved' in result and not 'errors' in result:
            fout = open('C:/Users/Public/Documents/jsontoaspacesuccess.txt', 'a')
            fout.write(filename + '\n' + json.dumps(result) + '\n\n')
            fout.close()
        elif 'errors' in result:
            fout = open('C:/Users/Public/Documents/jsontoaspaceerrors.txt', 'a')
            fout.write(filename + '\n' + json.dumps(result) + '\n\n')
            fout.close()
    print filename
