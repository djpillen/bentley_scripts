import requests
import json
import getpass

#global_aspace_url = 'http://localhost:8089'
#repository = '2'
#user = 'admin'
#password = 'admin'

class ArchivesSpace(object):
    def __init__(self):
        username = raw_input('Username:')
        password = getpass.getpass('Password:')
        try:
            aspace_url = global_aspace_url
        except:
            aspace_url = raw_input('ArchivesSpace Backend URL:')
        self.aspace_url = aspace_url
        auth = requests.post(aspace_url + '/users/'+username+'/login?password='+password)
        try:
            auth = auth.json()
            self.session = auth["session"]
        except:
            print auth.content
        

    def ead_to_json(self, filepath):
        headers = {'Content-type': 'text/xml; charset=utf-8', 'X-ArchivesSpace-Session': self.session}
        data = open(filepath, 'rb')
        eadtojson = requests.post(self.aspace_url + '/plugins/jsonmodel_from_format/resource/ead', headers=headers, data=data).json()
        return eadtojson

    def json_to_aspace(self, filepath):
        headers = {'Content-type': 'application/json', 'X-ArchivesSpace-Session': self.session}
        data = open(filepath, 'rb')
        jsontoresource = requests.post(self.aspace_url + '/repositories/2/batch_imports', headers=headers, data=data).json()
        return jsontoresource

    def get_subject(self, subject_id):
        subject = requests.get(self.aspace_url + '/subjects/' + str(subject_id)).json()
        return subject

    def get_subjects(self):
        subject_ids = requests.get(self.aspace_url + '/subjects?all_ids=true').json()
        for subject_id in subject_ids:
            subject = self.get_subject(subject_id)
            print subject_id, subject['title'].encode('utf-8')

    def post_subject(self, data):
        subject = requests.post(baseURL+'/subjects', headers=headers, data=data).json()
        return subject

    def get_person(self, person_id):
        person = requests.get(self.aspace_url + '/agents/people/' + str(person_id)).json()
        return person

    def get_people(self):
        person_ids = requests.get(self.aspace_url + '/agents/people?all_ids=true').json()
        for person_id in person_ids:
            person = self.get_person(person_id)
            print person_id, person['display_name']['sort_name'].encode('utf-8')

    def search(self):
        query = raw_input('Search query: ')
        headers = {'X-ArchivesSpace-Session':self.session}
        search = requests.get(self.aspace_url+'/repositories/2/search?page=1&q='+query,headers=headers).json()
        return search
