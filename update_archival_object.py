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

with open('C:/Users/Public/Documents/digital_object_csv.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        # We'll use an identifier and a file_uri from the csv to create the digital object
        identifier = row[3]
        file_uri = row[4]

        # Get the archival object's ASpace ref_id
        ref_id = row[2]

        # Search ASpace for the matching ref_id
        search = requests.get(aspace_url+'/repositories/2/search?page=1&q='+ref_id,headers=headers).json()

        # Grab the archival object uri from the search results
        archival_object_uri = search['results'][0]['uri']

        # Do a get request for the archival object and store the JSON
        archival_object_json = requests.get(aspace_url+archival_object_uri,headers=headers).json()

        # Continue only if the search-returned archival object's ref_id matches our starting ref_id
        if archival_object_json['ref_id'] == ref_id:

            # Add the archival object uri to the row in the csv to write it out at the end
            row.append(archival_object_uri)

            # Reuse the display string from the archival object as the title
            # Note: a better way of doing this would be to add the title and dates from the archival object separately
            # This also does not copy over any notes from the archival object
            display_string = archival_object_json['display_string']

            # Form the digital object JSON using the display string from the archival object and the identifier and the file_uri from the csv
            dig_obj = {'title':display_string,'digital_object_id':identifier,'file_versions':[{'file_uri':file_uri}]}
            dig_obj_data = json.dumps(dig_obj)

            # Post the digital object
            dig_obj_post = requests.post(aspace_url+'/repositories/2/digital_objects',headers=headers,data=dig_obj_data).json()

            print 'Digital Object Status', dig_obj_post['status']

            # Grab the digital object uri
            dig_obj_uri = dig_obj_post['uri']

            print 'Digital Object URI', dig_obj_uri

            # Add the digital object uri to the row in the csv to write it out at the end
            row.append(dig_obj_uri)

            # Build a new instance to add to the archival object, linking to the digital object
            dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}

            # Append the new instance to the existing archival object record
            archival_object_json['instances'].append(dig_obj_instance)
            archival_object_data = json.dumps(archival_object_json)

            # Repost the archival object
            archival_object_update = requests.post(aspace_url+archival_object_uri,headers=headers,data=archival_object_data).json()

            print archival_object_update

            # Write a new csv with all the info from the old one + the archival object and digital object uris
            with open('C:/Users/Public/Documents/digital_object_csv_updated.csv','ab') as csvout:
                writer = csv.writer(csvout)
                writer.writerow(row)
