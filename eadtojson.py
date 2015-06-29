import requests
import json
import os
from os.path import join


baseURL = 'http://localhost:8089'
repository = '2'
user = 'admin'
password = 'admin'

path = 'C:/Users/Public/Documents/test_eads'
outfilepath = 'C:/Users/Public/Documents/test_json'


for filename in os.listdir(path):
    auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
    session = auth["session"]

    headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session':session}
    data = open(join(path, filename), 'rb')
    eadtojson = requests.post(baseURL + '/plugins/jsonmodel_from_format/resource/ead', headers=headers, data=data).json()
    for result in eadtojson:
        if 'invalid_object' in result:

            fout = open('C:/Users/Public/Documentseadtojsonerrors.txt', 'a')
            fout.write(filename + '\n\n')
            fout.close()

    outfilename = filename + '.json'
    outfile = open(join(outfilepath, outfilename), 'w')
    json.dump(eadtojson, outfile)
    print filename
