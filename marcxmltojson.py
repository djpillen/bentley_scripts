import requests
import json
import os
from os.path import join
 

baseURL = 'http://localhost:8089'
repository = '2'
user = 'admin'
password = 'admin'
 
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]

headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session':session}

path = 'C:/Users/Public/Documents/ead-changes/marcxml_test'
for filename in os.listdir(path):
    data = open(join(path, filename), 'rb')
    eadtojson = requests.post(baseURL + '/plugins/jsonmodel_from_format/resource/marcxml', headers=headers, data=data).json()
    for result in eadtojson:
        if 'invalid_object' in result:
            fout = open('C:/Users/Public/Documents/eadtojsonerrors.txt', 'a')
            fout.write(filename + '\n' + str(result) + '\n\n')
            fout.close()
    outfilepath = 'C:/Users/Public/Documents/marcxml_test-json'
    outfilename = filename + '.json'
    outfile = open(join(outfilepath, outfilename), 'w')
    json.dump(eadtojson, outfile)
    print filename
