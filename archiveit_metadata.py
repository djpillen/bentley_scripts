import requests
from lxml import etree
from datetime import datetime
import os.path

all_collections = 'https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934'

last_exported_doc = 'last_exported_date.txt'
last_updated_date = datetime.strptime(lastUpdatedDate, '%Y-%m-%d %H:%M:%S')
if os.path.exists(last_exported_doc):
    with open('last_exported_date.txt','r').read() as last_exported:
        last_exported_date = datetime.strptime(last_exported,'%Y-%m-%d %H:%M:%S')
else:
    last_exported_date = datetime.utcfromtimestamp(0)

def parse_collection(collection):
    metadata = requests.get(collection)
    tree = etree.fromstring(metadata.text.encode('utf-8'))
    collections = tree.xpath('//collection')
    for collection in collections:
        coll_name = collection.xpath('./name')[0].text
        coll_id = collection.xpath('./id')[0].text
        seeds = collection.xpath('./seed')
        for seed in seeds:
            last_updated_date = seed.xpath('./lastUpdatedDate')[0].text
            public = seed.xpath('./public')[0].text
            if (last_exported_date < last_updated_date) and public == 'true':
                title = seed.xpath('./metadata/title')[0].text
                seed_url = seed.xpath('./metadata/url')[0].text
                archiveit_link = 'https://wayback.archive-it.org/' + coll_id + '/*/' + seed_url
                description = seed.xpath('./metadata/description')[0].text
                coverages = []
                coverage = seed.xpath('./metadata/coverage')
                for cover in coverage:
                    coverages.append(cover.text)
                subjects = seed.xpath('./subject')
                subject_list = []
                for subject in subjects:
                    subject_list.append(subject.text)
                personal_creators = []
                corporate_creator = []
                notes = []
                custom_metadata = seed.xpath('./metadata/customMetadata')
                for custom in custom_metadata:
                    if 'name' in custom.attrib:
                        if custom.attrib['name'] == 'corporate creator':
                            corporate_creators.append(custom.text)
                        elif custom.attrib['name'] == 'personal creator':
                            personal_creators.append(custom.text)
                            
                # Make the MARC
                record = etree.Element('record',nsmap={None:'http://www.loc.gov/MARC21/slim','xsi':'http://www.w3.org/2001/XMLSchema-instance'})
  
                
                    
            
        print coll_name, coll_id

parse_collection(all_collections)


with open('last_exported_date.txt','w') as last_exported:
    last_exported.write(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
