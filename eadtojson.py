import requests
import json
import os
from os.path import join
import time
from datetime import datetime

start_time = time.strftime("%Y-%m-%d %H:%M:%S %p")
program_start = datetime.now()

baseURL = 'http://localhost:8089'
repository = '2'
user = 'admin'
password = 'admin'

path = 'C:/Users/Public/Documents/test_eads'
outfilepath = 'C:/Users/Public/Documents/test_json'

attempts = 0
errors = []


for filename in os.listdir(path):
    attempts += 1
    auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
    session = auth["session"]

    headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session':session}
    data = open(join(path, filename), 'rb')
    eadtojson = requests.post(baseURL + '/plugins/jsonmodel_from_format/resource/ead', headers=headers, data=data).json()
    for result in eadtojson:
        if 'invalid_object' in result:
            fout = open('C:/Users/Public/Documentseadtojsonerrors.txt', 'a')
            fout.write(filename)
            fout.close()
    outfilename = filename + '.json'
    outfile = open(join(outfilepath, outfilename), 'w')
    json.dump(eadtojson, outfile)
    print filename

print "Conversion attempted on", str(attempts), "files"
print "Errors encountered in", str(len(errors)), "files"

print "Script start time:", start_time
print "Script end time:", time.strftime("%Y-%m-%d %H:%M:%S %p")
