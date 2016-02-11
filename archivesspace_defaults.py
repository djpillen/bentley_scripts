import requests
import time
import json
import getpass

def confirm_information(information):
	aspace_url = information['aspace_url']
	username = information['username']
	print "You are about to connect to an instance of ArchivesSpace using the following information"
	print "Backend URL:", aspace_url
	print "Username:", username
	correct = raw_input("Is this information correct? (y/n): ")
	if correct == 'y':
		return aspace_url, username
	else:
		print "Enter the correct information below"
		aspace_url = raw_input("ArchivesSpace URL: ")
		username = raw_input("Username: ")
		return aspace_url, username

def authenticate(aspace_url, username, password):
	auth = requests.post(aspace_url + '/users/' + username + '/login?password=' + password).json()
	if 'session' in auth:
		session = auth['session']
		headers = {'X-ArchivesSpace-Session':session}
		return True, headers
	else:
		return False, auth

def post_defaults(aspace_url, headers):
	bhl_repo = {
			'name':'Bentley Historical Library',
			'org_code':'MiU-H',
			'repo_code':'BHL',
			'parent_institution_name':'University of Michigan'
			}

	post_repo = requests.post(aspace_url + '/repositories',headers=headers,data=json.dumps(bhl_repo)).json()
	print post_repo

	'''
	base_profile = {
		'name':'',
		'extent_dimension':'height',
		'dimension_units':'inches',
		'height':'0',
		'width':'0',
		'depth':'0'
	}

	profile_names = ['box','folder','volume','reel','map-case','panel','sound-disc','tube','item','object','bundle']

	for profile_name in profile_names:
		container_profile = base_profile
		container_profile['name'] = profile_name
		profile_post = requests.post(aspace_url + '/container_profiles',headers=headers,data=json.dumps(container_profile)).json()
		print profile_post
	'''

	mhc_classification = {'title':'Michigan Historical Collections','identifier':'MHC'}
	uarp_classification = {'title':'University Archives and Records Program','identifier':'UARP'}
	rcs_classification = {'title':'Records Center Storage','identifier':'RCS'}

	for classification in [mhc_classification, uarp_classification, rcs_classification]:
		classification_post = requests.post(aspace_url + '/repositories/2/classifications',headers=headers,data=json.dumps(classification)).json()
		print classification_post

	subject_sources = requests.get(aspace_url + '/config/enumerations/23',headers=headers).json()
	subject_sources['values'].extend(['lcnaf','lctgm','aacr2'])
	update_subject_sources = requests.post(aspace_url + '/config/enumerations/23',headers=headers,data=json.dumps(subject_sources)).json()
	print update_subject_sources

	name_sources = requests.get(aspace_url + '/config/enumerations/4',headers=headers).json()
	name_sources['values'].append('lcnaf')
	update_name_sources = requests.post(aspace_url + '/config/enumerations/4',headers=headers,data=json.dumps(name_sources)).json()
	print update_name_sources


	repo_preferences = {
		'repository':{'ref':'/repositories/2'},
		'defaults':{'publish':True}
		}

	repo_preferences_post = requests.post(aspace_url + '/repositories/2/preferences',headers=headers, data=json.dumps(repo_preferences)).json()
	print repo_preferences_post


def main():
	pre_configured_info = {'aspace_url':'http://141.211.39.87:8089', 'username':'admin'}
	aspace_url, username = confirm_information(pre_configured_info)
	password = getpass.getpass("Password:")
	status, auth_info = authenticate(aspace_url, username, password)
	if status:
		post_defaults(aspace_url, auth_info)
	else:
		print "Problem establishing a session"
		print auth_info

main()