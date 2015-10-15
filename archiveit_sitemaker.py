import requests
from lxml import etree
import os
from os.path import join

path = 'U:/web_archives'
collection_feed_url = 'https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934'

with requests.Session() as s:
    collection_feed = s.get(collection_feed_url)

collection_metadata = etree.fromstring(collection_feed.text.encode('utf-8'))
tree = etree.ElementTree(collection_metadata)
collections = tree.xpath('//collection')
for collection in collections:
    collection_title = collection.xpath('./name')[0].text
    print 'Checking ' + collection_title
    with open(join(path,'sitemaker.txt'),'a') as outfile:
        outfile.write(collection_title + '\n\n')
    seeds = collection.xpath('.//seed')
    for seed in seeds:
        url = seed.xpath('./url')[0].text
        if 'sitemaker' in url:
            if seed.xpath('./active')[0].text == 'true':
                print url
                with open(join(path,'sitemaker.txt'),'a') as outfile:
                    outfile.write(url + '\n')
    with open(join(path,'sitemaker.txt'),'a') as outfile:
        outfile.write('\n\n')
