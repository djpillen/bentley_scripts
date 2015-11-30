import requests
from lxml import etree
import os
from os.path import join
from datetime import datetime
import csv

def find_existing_file(archiveit_dir,saved_metadata_base):
	print "Checking for existing metadata"
	collectionFeed = False
	for filename in os.listdir(archiveit_dir):
		if filename.startswith(saved_metadata_base):
			collectionFeed = join(archiveit_dir,filename)
	if collectionFeed:
		print "Existing metadata found at {0}".format(collectionFeed)
	else:
		print "No existing metadata found"
	return collectionFeed

def analyze_timestamp(collectionFeed,today_object):
	print "Analyzing timestamp on existing collectionFeed"
	date_and_extension = collectionFeed.split('_')[-1]
	saved_date = date_and_extension.replace('.xml','')
	saved_date_object = datetime.strptime(saved_date,"%Y-%m-%d")
	difference = today_object - saved_date_object
	print "Difference:", difference.days
	return difference.days

def fetch_metadata(archiveit_dir, saved_metadata_base, today):
	print "Fetching metadata from Archive-It"
	archiveit_metadata_url = 'https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934'
	metadata = requests.get(archiveit_metadata_url)
	tree = etree.fromstring(metadata.text.encode('utf-8'))
	archiveit_metadata_file = join(archiveit_dir,saved_metadata_base+today+'.xml')
	with open(archiveit_metadata_file,'w') as metadata_file:
		metadata_file.write(etree.tostring(tree))
	print "Metadata file saved at", archiveit_metadata_file
	return archiveit_metadata_file

def find_missing_metadata(archiveit_dir, metadata):
	print "Checking for missing metadata"
	missing_metadata_csv = join(archiveit_dir,'missing_metadata.csv')
	if os.path.exists(missing_metadata_csv):
		os.remove(missing_metadata_csv)
	collections = metadata.xpath('//collection')
	with open(missing_metadata_csv,'ab') as csvfile:
		writer = csv.writer(csvfile)
		for collection in collections:
			collection_name = collection.xpath('./name')[0].text
			seeds = metadata.xpath('//collection/seeds/seed')
			for seed in seeds:
				public = seed.xpath('./public')[0].text
				metadata = seed.xpath('./metadata')[0]
				url = seed.xpath('./url')[0].text
				metadata_elements = metadata.xpath('./*')
				metadata_element_names = [metadata_element.tag for metadata_element in metadata_elements]
				if len(metadata_elements) < 2:
					writer.writerow([collection_name,url])
					print collection_name, url

def main():
	archiveit_dir = 'C:/Users/djpillen/GitHub/test_dir/archive-it'
	saved_metadata_base = 'archive-it_collectionFeed_'
	today_object = datetime.now()
	today = today_object.strftime("%Y-%m-%d")
	collectionFeed = find_existing_file(archiveit_dir,saved_metadata_base)
	if collectionFeed:
		difference = analyze_timestamp(collectionFeed,today_object)
	if not collectionFeed or difference >= 7:
		metadata_file = fetch_metadata(archiveit_dir, saved_metadata_base, today)
		metadata = etree.parse(metadata_file)
	else:
		metadata = etree.parse(collectionFeed)
	find_missing_metadata(archiveit_dir, metadata)

main()