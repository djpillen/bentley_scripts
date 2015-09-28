import requests
import json
from os.path import join
import time
from datetime import datetime
import random

start_time = datetime.now()


aspace_url = 'http://localhost:8089'
username = 'admin'
password = 'admin'

ead_directory = 'C:/Users/Public/Documents/aspace_exports_unpublished'

auth = requests.post(aspace_url+'/users/admin/login?password=' + password + '&expired=false').json()
session = auth['session']
headers = {'X-ArchivesSpace-Session':session}

all_ids = requests.get(aspace_url+'/repositories/2/resources?all_ids=true', headers=headers).json()


the_id = 2209
resource_id = the_id

ead = requests.get(aspace_url+'/repositories/2/resource_descriptions/'+str(resource_id)+'.xml?include_unpublished=true&include_daos=true&numbered_cs=true',headers=headers, stream=True)
with open(join(ead_directory,str(resource_id)+'.xml'),'wb') as ead_out:
     for chunk in ead.iter_content(10240):
            ead_out.write(chunk)
print "Wrote {0}".format(resource_id)

print "Done"

end_time = datetime.now()

print "Script start time:", start_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script end time:", end_time.strftime("%Y-%m-%d %H:%M:%S %p")
print "Script running time:", end_time - start_time
