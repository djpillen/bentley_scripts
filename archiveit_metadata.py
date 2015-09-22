import requests
from lxml import etree
from datetime import datetime

all_collections = 'https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934'

last_exported_doc = 'last_exported_date.txt'
last_updated_date = datetime.strptime(lastUpdatedDate, '%Y-%m-%d %H:%M:%S')
if last_exported_doc:
    with open('last_exported_date.txt','r').read() as last_exported:
        last_exported_date = datetime.strptime(last_exported,'%Y-%m-%d %H:%M:%S')
else:
    last_exported_date = datetime.utcfromtimestamp(0)
date_difference = last_exported_date - last_updated_date
if last_exported_date < last_updated_date:
    continue

def parse_collection(collection):
    metadata = requests.get(collection)
    tree = etree.fromstring(metadata.text.encode('utf-8'))
    collections = tree.xpath('//collection')
    for collection in collections:
        coll_name = collection.xpath('./name')[0].text
        coll_id = collection.xpath('./id')[0].text
        print coll_name, coll_id

parse_collection(all_collections)


with open('last_exported_date.txt','w') as last_exported:
    last_exported.write(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
