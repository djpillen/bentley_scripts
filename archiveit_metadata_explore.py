import requests
from lxml import etree


metadata = requests.get('https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934')
tree = etree.fromstring(metadata.text.encode('utf-8'))

seeds = tree.xpath('//seed')

multiple = {'corp':0,'pers':0,'notes':0}

for seed in seeds:
    corp = 0
    pers = 0
    notes = 0
    title = seed.xpath('./metadata/title')
    if title:
        title = title[0].text
    else:
        title = 'No title'
    custom_metadata = seed.xpath('./metadata/customMetadata')
    for c in custom_metadata:
        if 'name' in c.attrib:
            if c.attrib['name'] == 'corporate creator':
                corp += 1
            elif c.attrib['name'] == 'personal creator':
                pers += 1
            elif c.attrib['name'] == 'note':
                notes += 1
    if corp > 1:
        multiple['corp'] += 1
    if pers > 1:
        multiple['pers'] += 1
    if notes > 1:
        multiple['notes'] += 1

print multiple