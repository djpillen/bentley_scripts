import requests
import json
import os
from os.path import join
import time
from datetime import datetime

start_time = datetime.now()

baseURL = 'http://localhost:8089'
repository = '2'
user = 'admin'
password = 'admin'

path = 'C:/Users/Public/Documents/test_2'
outfilepath = 'C:/Users/Public/Documents/test_json_2'

attempts = 0
errors = 0


for filename in os.listdir(path):
    attempts += 1
    auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
    session = auth["session"]

    headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session':session}
    data = open(join(path, filename), 'rb')
    eadtojson = requests.post(baseURL + '/plugins/jsonmodel_from_format/resource/ead', headers=headers, data=data).json()
    for result in eadtojson:
        if 'invalid_object' in result:
            fout = open('C:/Users/Public/Documents/eadtojsonerrors-2.txt', 'a')
            fout.write(filename + '\n')
            fout.close()
            errors += 1
    outfilename = filename + '.json'
    outfile = open(join(outfilepath, outfilename), 'w')
    json.dump(eadtojson, outfile)
    print filename

end_time = datetime.now()

print "Conversion attempted on", str(attempts), "files"
print "Errors encountered in", str(errors), "files"

print "Script start time:", start_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script end time:", end_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script running time:", end_time - start_time
