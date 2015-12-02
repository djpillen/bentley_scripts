import requests
import json
import os
from os.path import join

github_api = 'https://api.github.com'

latest_release_api = github_api + '/repos/archivesspace/archivesspace/releases/latest'

save_location = 'C:/Users/djpillen/Downloads'

with requests.Session() as s:
	print "Finding the latest release"
	latest_release_json = requests.get(latest_release_api).json()
	latest_release_name = latest_release_json['assets'][0]['name']
	latest_release_url = latest_release_json['assets'][0]['browser_download_url']
	print "Latest release url:",latest_release_url
	print "Latest release name:",latest_release_name
	save_file = join(save_location,latest_release_name)
	if not os.path.exists(save_file):
		latest_release_zip = s.get(latest_release_url)
		with open(save_file,'wb') as outfile:
			print "Saving latest release to", save_file
			outfile.write(latest_release_zip.content)
	else:
		print "Latest release already downloaded"


