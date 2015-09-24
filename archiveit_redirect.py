import os
from os.path import join
import requests
from lxml import etree



def get_seed_metadata(starting_seed):
    with requests.Session() as s:
        collection_feed = s.get('https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934')
    tree = etree.fromstring(collection_feed.text.encode('utf-8'))
    seeds = tree.xpath('//seed')
    for seed in seeds:
        url = seed.xpath('./url')[0].text
        if url == starting_seed:
            starting_metadata = seed
            break
    skip = ['createdDate','lastUpdatedDate','active','public','note','url']
    seed_metadata = []
    new_url = {}
    new_url['url'] = new_seed
    seed_metadata.append(new_url)
    for elem in seed.xpath('.//*'):
        if elem.text is not None and not elem.tag in skip and not 'name' in elem.attrib:
            elem_metadata = {}
            elem_name = elem.tag
            elem_text = elem.text
            elem_metadata[elem_name] = elem_text
            seed_metadata.append(elem_metadata)
        elif 'name' in elem.attrib:
            if elem.attrib['name'] not in skip:
                elem_metadata = {}
                elem_name = elem.attrib['name']
                elem_text = elem.text
                elem_metadata[elem_name] = elem_text
                seed_metadata.append(elem_metadata)
    new_note = {}
    new_note['Note'] = "Seed created due to redirect from {0}".format(starting_seed)
    seed_metadata.append(new_note)
    process_note = {}
    process_note['Note to processor'] = "Be sure to inactivate the old seed ({0}) and add a note regarding the creation of a new seed".format(starting_seed)
    seed_metadata.append(process_note)
    with open('U:/web_archives/redirects/new_data.txt','a') as redirect_txt:
        for element in seed_metadata:
            for field in element:
                element_text = element[field]
                redirect_txt.write(field + ': ' + element_text + '\n')

starting_seed = raw_input('Enter the starting seed: ')
new_seed = raw_input('Enter the new seed: ')

get_seed_metadata(starting_seed)
