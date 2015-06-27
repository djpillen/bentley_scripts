
"""
Get location info:

curl -H "X-ArchivesSpace-Session:$TOKEN" http://localhost:8089/locations/3
{"lock_version":1,"building":"Bentley Historical Library","title":"Bentley Historical Library [123454, Y: 3]","barcode":"123454","coordinate_1_label":"Y","coordinate_1_indicator":"3","created_by":"admin","last_modified_by":"admin","create_time":"2015-05-18T13:49:32Z","system_mtime":"2015-06-09T15:00:34Z","user_mtime":"2015-06-09T15:00:34Z","jsonmodel_type":"location","external_ids":[],"uri":"/locations/3"}

Post a location:

curl -H "X-ArchivesSpace-Session:$TOKEN" -d '{"building":"Bentley Historical Library", "coordinate_1_label":"B", "coordinate_1_indicator":"123"}' http://localhost:8089/locations
{"status":"Created","id":12,"lock_version":0,"stale":true,"uri":"/locations/12","warnings":[]}


"""

import requests
import json
import csv
 

baseURL = 'http://localhost:8089'
repository = '2'
user = 'admin'
password = 'admin'


auth = requests.post('http://localhost:8089/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

location_file = 'locations.csv'

with open('locations.csv','rb') as location_file:
    reader = csv.reader(location_file)
    for row in reader:
        building = str(row[0])
        coordinate_label = str(row[1])
        coordinate_indicator = str(row[2])
        barcode = str(row[3])
        data = json.dumps({'building':building, 'coordinate_1_label':coordinate_label, 'coordinate_1_indicator':coordinate_indicator,'barcode':barcode})
        locations = requests.post('http://localhost:8089/locations', headers=headers, data=data).json()
        print locations
