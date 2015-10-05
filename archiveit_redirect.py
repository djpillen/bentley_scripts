import os
from os.path import join
import requests
from lxml import etree
import csv
import re
import HTMLParser


redirect_csv = 'U:/web_archives/jobs/master_redirects.csv'

redirect_dict = {}

with open(redirect_csv,'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader,None)
    for row in reader:
        job = row[0]
        seed = row[1]
        redirect = row[2]
        if job not in redirect_dict:
            redirect_dict[job] = {}
        redirect_dict[job][seed] = redirect


def get_redirect_metadata(redirect_dict):
    jobs_dir = 'U:/web_archives/jobs'
    skip = ['createdDate','lastUpdatedDate','active','public','note','url']
    for job in redirect_dict:
        job_dir = join(jobs_dir,job)
        with open(join(job_dir,'seedstatus.csv'),'rb') as csvfile:
            reader = csv.reader(csvfile)
            first_row = reader.next()
            collection_string = first_row[0]
            collection_id = re.findall(r'(\d+)\t',collection_string)[0]
        starting_seeds = {}
        for seed in redirect_dict[job]:
            starting_seeds[seed] = ''
        with requests.Session() as s:
            collection_feed = s.get('https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934&collectionId=' + collection_id)
        collection_metadata = etree.fromstring(collection_feed.text.encode('utf-8'))
        tree = etree.ElementTree(collection_metadata)
        seeds = tree.xpath('//seed')
        for seed in seeds:
            url = seed.xpath('./url')[0].text
            if url in starting_seeds:
                starting_seeds[url] = tree.getpath(seed)
        redirect_metadata = []
        add_seeds = []
        redirect_investigate = []
        entity_parser = HTMLParser.HTMLParser()
        for seed in starting_seeds:
            if len(starting_seeds[seed]) > 0:
                new_seed = redirect_dict[job][seed]
                add_seeds.append(new_seed)
                seed_metadata = {}
                seed_path = starting_seeds[seed]
                seed_element = tree.xpath(seed_path)[0]
                for elem in seed_element.xpath('.//*'):
                    if elem.text is not None and not elem.tag in skip and not 'name' in elem.attrib:
                        elem_name = elem.tag
                        elem_text = entity_parser.unescape(elem.text.replace('&#8220;','"').replace('&#8221;','"'))
                        if elem_name not in seed_metadata:
                            seed_metadata[elem_name] = []
                        seed_metadata[elem_name].append(elem_text.encode('utf-8'))
                    elif 'name' in elem.attrib:
                        if elem.attrib['name'] not in skip:
                            elem_name = elem.attrib['name']
                            elem_text = entity_parser.unescape(elem.text.replace('&#8220;','"').replace('&#8221;','"'))
                            if elem_name not in seed_metadata:
                                seed_metadata[elem_name] = []
                            seed_metadata[elem_name].append(elem_text.encode('utf-8'))
                seed_metadata['url'] = []
                seed_metadata['url'].append(new_seed)
                seed_metadata['Note'] = []
                seed_metadata['Note'].append("QA Note: This seed was created due to redirects from the previous seed URL. Previous captures under seed URL " + seed)
                redirect_metadata.append(seed_metadata)
            else:
                redirect_investigate.append(seed)
        with open(join(jobs_dir, job + '_deactivate.txt'),'a') as deactivate_txt:
            deactivate_txt.write('\n'.join([seed for seed in starting_seeds]))
        with open(join(jobs_dir,job + '_addseeds.txt'),'a') as add_seeds_txt:
            add_seeds_txt.write('\n'.join([seed for seed in add_seeds]))
        with open(join(jobs_dir,job + '_redirect_investigate.txt'),'a') as investigate_txt:
            investigate_txt.write('\n'.join([seed for seed in redirect_investigate]))

        header_order = ['url','Title','Subject','Personal Creator','Corporate Creator','Coverage','Description','Publisher','Note']
        redirect_csv = join(jobs_dir,job + '_redirect_metadata.csv')
        header_counts = {}
        for seed in redirect_metadata:
            for element in seed:
                count = len(seed[element])
                elem_lower = element.lower()
                if element not in header_counts:
                    header_counts[element] = count
                elif count > header_counts[element]:
                    header_counts[element] = count
        for element in header_order:
            elem_lower = element.lower()
            if element not in header_counts and elem_lower not in header_counts:
                header_counts[element] = 1
        for seed in redirect_metadata:
            for element in header_counts:
                if element not in seed:
                    seed[element] = []
            for element in seed:
                current_count = len(seed[element])
                header_count = header_counts[element]
                difference = header_count - current_count
                if difference > 0:
                    seed[element].extend([''] * difference)
        header_row = []
        header_counts_lower = {k.lower():v for k,v in header_counts.items()}
        for element in header_order:
            elem_lower = element.lower()
            header_row.extend([element] * header_counts_lower[elem_lower])
        with open(redirect_csv,'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header_row)
        for seed in redirect_metadata:
            row = []
            for element in header_order:
                elem_lower = element.lower()
                if element in seed:
                    row.extend([item for item in seed[element]])
                elif elem_lower in seed:
                    row.extend([item for item in seed[elem_lower]])
            with open(redirect_csv,'ab') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)


get_redirect_metadata(redirect_dict)






"""
    print "Getting metadata for redirected seeds"
    redirect_dir = join(job_dir,'redirects')
    starting_seeds = {}
    skip = ['createdDate','lastUpdatedDate','active','public','note','url']
    elem_names = []
    for url in seed_status_dict['redirects']:
        starting_seeds[url] = ''
    with requests.Session() as s:
        collection_feed = s.get('https://partner.archive-it.org/seam/resource/collectionFeed?accountId=934')
    tree = etree.fromstring(collection_feed.text.encode('utf-8'))
    seeds = tree.xpath('//seed')
    for seed in seeds:
        url = seed.xpath('./url')[0].text
        if url in starting_seeds:
            starting_seeds[url] = tree.getpath(seed)
    redirect_metadata = []
    for seed in starting_seeds:
        seed_metadata = {}
        seed_path = starting_seeds[seed]
        for elem in seed_path.xpath('.//*'):
            if elem.text is not None and not elem.tag in skip and not 'name' in elem.attrib:
                elem_name = elem.tag
                elem_text = elem.text
                if elem_name not in seed_metadata:
                    seed_metadata[elem_name = []
                seed_metadata[elem_name].append(elem_text)
            elif 'name' in elem.attrib:
                if elem.attrib['name'] not in skip:
                    elem_name = elem.attrib['name']
                    elem_text = elem.text
                    if elem_name not in seed_metadata:
                        seed_metadata[elem_name] = []
                    seed_metadata[elem_name].append(elem_text)
        seed_metadata['url'] = []
        seed_metadata['url'].append(seed_status_dict['redirects'][seed])
        seed_metadata['Note'] = []
        seed_metadata['Note'].append("Seed created due to redirect from " + seed)
        redirect_metadata.append(seed_metadata)
        with open(join(redirect_dir,seed + '.txt'),'a') as redirect_txt:
            for element in seed_metadata:
                for field in element:
                    element_text = element[field]
                    redirect_txt.write(field + ': ' + element_text + '\n')


def get_seed_metadata(starting_seed, new_seed):
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

get_seed_metadata(starting_seed, new_seed)
"""
