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

base_dir = 'C:/Users/djpillen/GitHub/test_run'

ead_path = join(base_dir,'ead')
json_path = join(base_dir,'json')

attempts = 0
errors = 0


for filename in os.listdir(ead_path):
    if filename + '.json' not in os.listdir(json_path):
        attempts += 1
        auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
        session = auth["session"]

        headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session':session}
        data = open(join(ead_path, filename), 'rb')
        eadtojson = requests.post(baseURL + '/plugins/jsonmodel_from_format/resource/ead', headers=headers, data=data).json()
        for result in eadtojson:
            if 'invalid_object' in result:
                fout = open(join(base_dir,'eadtojsonerrors.txt'), 'a')
                fout.write(filename + '\n')
                fout.close()
                errors += 1
        with open(join(json_path,filename+'.json'),'w') as json_out:
            json_out.write(json.dumps(eadtojson))
        print filename

end_time = datetime.now()

print "Conversion attempted on", str(attempts), "files"
print "Errors encountered in", str(errors), "files"

print "Script start time:", start_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script end time:", end_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script running time:", end_time - start_time

converter_stats = "Script start time: " + start_time.strftime("%Y-%m-%d %H:%M:%S %p") + "\n" + "Script end time: " +  end_time.strftime("%Y-%m-%d %H:%M:%S %p") + "\n" + "Script running time: " + str(end_time - start_time)
stats_file = open(join(base_dir,'converter_stats.txt'),'w')
stats_file.write(converter_stats)
stats_file.close()
