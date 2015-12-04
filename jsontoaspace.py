import requests
import os
from os.path import join
import json
import time
from datetime import datetime

start_time = datetime.now()

baseURL = 'http://141.211.39.87:8089'
repository = '2'
user = 'admin'
password = 'admin'

def authenticate():
    auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
    session = auth["session"]
    headers = {'Content-type': 'application/json', 'X-ArchivesSpace-Session': session}
    return headers

errors = []
successes = []

base_dir = 'C:/Users/djpillen/GitHub/test_run'
path = join(base_dir,'json')
outfilepath = join(base_dir,'resources')

for filename in os.listdir(path):
    headers = authenticate()
    data = open(join(path, filename), 'rb')
    jsontoresource = requests.post(baseURL + '/repositories/2/batch_imports', headers=headers, data=data).json()
    for result in jsontoresource:
        if 'saved' in result and not 'errors' in result:
            if filename not in successes:
                successes.append(filename)
        elif 'errors' in result:
            if filename not in errors:
                errors.append(filename)
    with open(join(outfilepath,filename),'w') as json_out:
        json_out.write(json.dumps(jsontoresource))
    print filename

for filename in errors:
    fout = open(join(base_dir,'jsontoaspaceerrors.txt'), 'a')
    fout.write(filename + '\n')
    fout.close()

for filename in successes:
    fout = open(join(base_dir,'jsontoaspacesuccess.txt'), 'a')
    fout.write(filename + '\n')
    fout.close()

end_time = datetime.now()

print "Successfully imported:", str(len(successes))
print "Errors encountered in", str(len(errors)), "files"

print "Script start time:", start_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script end time:", end_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script running time:", end_time - start_time

importer_stats = "Script start time: " + start_time.strftime("%Y-%m-%d %H:%M:%S %p") + "\n" + "Script end time: " +  end_time.strftime("%Y-%m-%d %H:%M:%S %p") + "\n" + "Script running time: " + str(end_time - start_time)
stats_file = open(join(base_dir,'importer_stats.txt'),'w')
stats_file.write(importer_stats)
stats_file.close()
