import requests
import json
import csv

# This script will create a new digital object and link it as an instance to an existing archival object
# This was written under the assumption that you might have a csv (or similar), exported from ASpace or
# compiled from an ASpace exported EAD, with an existing archival object's refid. Using only the refid,
# this will use the ASpace API to search for the existing archival object, retrieve its URI, store the archival
# object's JSON, create a new digital object using the title from the archival object and an identifier (also from the CSV),
# grab the URI for the newly created digital object, add the link as an instance to the archival object JSON,
# and repost the archival object to ASpace using the update archival object endpoint


aspace_url = 'http://localhost:8089'
username= 'admin'
password = 'admin'

auth = requests.post(aspace_url+'/users/'+username+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

with open(archival_objects_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        identifier = row[3]
        # Get the archival object's ASpace ref_id
        ref_id = row[2]
        # Search ASpace for the matching ref_id
        search = requests.get(aspace_url+'/repositories/2/search?page=1&q='+ref_id,headers=headers).json()
        archival_object_uri = search['results'][0]['uri']
        # Store the JSON for the archival object
        archival_object_json = requests.get(aspace_url+archival_object_uri,headers=headers).json()
        row.append(archival_object_uri)
        display_string = archival_object_json['display_string']
        # Form the digital object JSON
        dig_obj = {'title':display_string,'digital_object_id':identifier}

        dig_obj_data = json.dumps(dig_obj)
        # Post the digital object
        dig_obj_post = requests.post(aspace_url+'/repositories/2/digital_objects',headers=headers,data=dig_obj_data).json()

        print 'Digital Object Status', dig_obj_post['status']
        # Grab the digital object uri
        dig_obj_uri = dig_obj_post['uri']

        print 'Digital Object URI', dig_obj_uri

        row.append(dig_obj_uri)
        # Build a new instance, linking to the digital object
        dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}
        # Append the new instance to the existing archival object record
        archival_object_json['instances'].append(dig_obj_instance)

        archival_object_data = json.dumps(archival_object_json)
        # Repost the archival object
        archival_object_update = requests.post(aspace_url+archival_object_uri,headers=headers,data=archival_object_data).json()

        print archival_object_update

        with open(archival_objects_updated,'ab') as csvout:
            writer = csv.writer(csvout)
            writer.writerow(row)
