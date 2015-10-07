import os
from os.path import join
import requests
from lxml import etree
import csv
import re
import HTMLParser

def get_redirect_metadata(redirect_dict, collection_id, redirect_dir):
    skip = ['createdDate','lastUpdatedDate','active','public','note','url']
    starting_seeds = {}
    for seed in redirect_dict:
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
    add_deactivate = {}
    redirect_investigate = {}
    entity_parser = HTMLParser.HTMLParser()
    for seed in starting_seeds:
        if len(starting_seeds[seed]) > 0:
            new_seed = redirect_dict[seed]
            add_deactivate[seed] = new_seed
            seed_metadata = {}
            seed_path = starting_seeds[seed]
            seed_element = tree.xpath(seed_path)[0]
            for elem in seed_element.xpath('.//*'):
                if elem.text is not None and not elem.tag in skip and not 'name' in elem.attrib:
                    elem_name = elem.tag
                    elem_text = entity_parser.unescape(elem.text.replace('&#8220;','"').replace('&#8221;','"').replace('&#8217;',"'"))
                    if elem_name not in seed_metadata:
                        seed_metadata[elem_name] = []
                    seed_metadata[elem_name].append(elem_text.encode('utf-8'))
                elif 'name' in elem.attrib:
                    if elem.attrib['name'] not in skip:
                        elem_name = elem.attrib['name']
                        elem_text = entity_parser.unescape(elem.text.replace('&#8220;','"').replace('&#8221;','"').replace('&#8217;',"'"))
                        if elem_name not in seed_metadata:
                            seed_metadata[elem_name] = []
                        seed_metadata[elem_name].append(elem_text.encode('utf-8'))
            seed_metadata['url'] = []
            seed_metadata['url'].append(new_seed)
            seed_metadata['Note'] = []
            seed_metadata['Note'].append("QA NOTE: This seed was created as a result of the previous seed URL redirecting to this URL. Previous captures under seed URL " + seed)
            redirect_metadata.append(seed_metadata)
        else:
            redirect_investigate[seed] = redirect_dict[seed]
    with open(join(redirect_dir,'add_and_deactivate.csv'),'ab') as add_deactivate_csv:
        writer = csv.writer(add_deactivate_csv)
        writer.writerow(['Add','Deactivate','Deactivation Note'])
        for seed, new_seed in add_deactivate.items():
            writer.writerow([new_seed, seed, 'QA NOTE: Seed deactivated. Seed URL redirects to ' + new_seed + '. A new seed with the redirected seed URL has been added.'])
    if len(redirect_investigate) > 0:
        with open(join(redirect_dir,'redirect_investigate.csv'),'ab') as investigate_csv:
            writer = csv.writer(investigate_csv)
            writer.writerow(['Seed URL','Redirect URL'])
            for seed, new_seed in redirect_investigate.items():
                writer.writerow([seed, new_seed])
    header_order = ['url','Title','Subject','Personal Creator','Corporate Creator','Coverage','Description','Publisher','Note']
    redirect_csv = join(redirect_dir,'redirect_metadata.csv')
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


def main():
    job_numbers = raw_input('Enter a comma separated list of job numbers: ')
    base_dir = raw_input('Enter the directory in which job files are saved (e.g., U:/web_archives/jobs): ')
    jobs = [job.strip() for job in job_numbers.split(',')]
    for job in jobs:
        redirect_dict = {}
        job_dir = join(base_dir,job)
        with open(join(job_dir,'seedstatus.csv'),'rb') as csvfile:
            reader = csv.reader(csvfile)
            first_row = reader.next()
            collection_string = first_row[0]
            collection_id = re.findall(r'(\d+)\t',collection_string)[0]
        redirect_dir = join(job_dir,'redirects')
        redirect_csv = join(redirect_dir,'redirect_information.csv')
        with open(redirect_csv,'rb') as redirect_csv:
            reader = csv.reader(redirect_csv)
            next(reader,None)
            for row in reader:
                seed = row[0].strip()
                redirect = row[1].strip()
                redirect_dict[seed] = redirect
        get_redirect_metadata(redirect_dict,collection_id,redirect_dir)

main()
