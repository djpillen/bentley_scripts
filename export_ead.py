#!/usr/bin/env python

# All credit for this script to Hillel Arnold
# https://github.com/RockefellerArchiveCenter/scripts/blob/master/archivesspace/asExport-ead.py

import os, requests, json, sys, logging

# the base URL of your ArchivesSpace installation
baseURL = 'http://localhost:8089'
# the id of your repository
repository = '2'
# the username to authenticate with
user = 'admin'
# the password for the username above
password = 'admin'
# parses arguments, if any. This allows you to pass in an string to match against resource IDs
exportIds = sys.argv[1]
# export destination
destination = 'C:/Users/Public/Documents/aspace_exports'
logging.basicConfig(filename='C:/Users/Public/Documents/ead_export_log.txt',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# authenticates the session
def authenticate():
    auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
    session = auth["session"]
    headers = {'X-ArchivesSpace-Session':session}
    return headers

headers = authenticate()

# Gets the IDs of all resources in the repository
logging.info('Getting a list of resources')
resourceIds = requests.get(baseURL + '/repositories/'+repository+'/resources?all_ids=true', headers=headers)

# Exports EAD for all resources whose IDs contain argument
for resourceId in resourceIds.json():
    if not requests.get(baseURL + '/repositories/'+repository+'/resources/' + str(resourceId), headers=headers):
        headers = authenticate()
    resource = (requests.get(baseURL + '/repositories/'+repository+'/resources/' + str(resourceId), headers=headers)).json()
    resourceID0 = resource["id_0"]
    if exportIds:
        if exportIds in resourceID0:
            logging.info('Exporting ' + resourceID0)
            ead = requests.get(baseURL + '/repositories/'+repository+'/resource_descriptions/'+str(resourceId)+'.xml', headers=headers, stream=True)
            if not os.path.exists(destination):
                os.makedirs(destination)
            with open(destination+resourceID0+'.xml', 'wb') as f:
                for chunk in ead.iter_content(10240):
                    f.write(chunk)
            f.close
    else:
        logging.info('Exporting ' + resourceID0)
        ead = requests.get(baseURL + '/repositories/'+repository+'/resource_descriptions/'+str(resourceId)+'.xml', headers=headers, stream=True)
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(destination+resourceID0+'.xml', 'wb') as f:
            for chunk in ead.iter_content(10240):
                f.write(chunk)
        f.close
logging.info('Done!')
