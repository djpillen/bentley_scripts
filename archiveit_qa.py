import requests
import csv
import re
import os
from os.path import join
import zipfile
import random
from lxml import etree

def make_directories(base_dir, job):
    print "Making necessary directories"
    job_dir = join(base_dir,job)
    os.makedirs(job_dir)
    os.makedirs(join(job_dir,'zips'))
    os.makedirs(join(job_dir,'crawled_queued'))
    os.makedirs(join(job_dir,'repeating_directories_all'))
    os.makedirs(join(job_dir,'repeating_directories_checked'))
    os.makedirs(join(job_dir,'statuses'))
    return job_dir

def get_base_reports(job, job_dir):
    print "Getting host and seed reports"
    hosts_report = requests.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=host')
    with open(join(job_dir,'hosts.csv'),'wb') as host_csv:
        host_csv.write(hosts_report.content)
    status_report = requests.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=seed')
    with open(join(job_dir,'seedstatus.csv'),'wb') as status_csv:
        status_csv.write(status_report.content)
    source_report = requests.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=source')
    with open(join(job_dir,'seedsource.csv'),'wb') as source_csv:
        source_csv.write(source_report.content)

def get_host_info(job_dir):
    print "Building a dictionary and list of hosts"
    host_dict = {}
    host_list = []
    with open(join(job_dir,'hosts.csv'),'rb') as host_csv:
        reader = csv.reader(host_csv)
        next(reader,None)
        next(reader,None)
        for row in reader:
            host = row[0]
            crawled = row[1]
            data = row[2]
            queued = row[6]
            if host.endswith(':'):
                host = re.sub(r':$','',host)
            host_dict[host] = {}
            host_dict[host]['crawled'] = int(crawled)
            host_dict[host]['queued'] = int(queued)
            host_dict[host]['data'] = int(data)
            host_list.append(host)
    return host_dict, host_list

def get_crawl_reports(job_dir, job, host, report_type):
    print "Downloading {0} report for {1}".format(report_type, host)
    url = 'https://partner.archive-it.org/seam/resource/' + report_type + 'ByHost?crawlJobId=' + job + '&host=' + host
    if url.endswith(':'):
        re.sub(r':$',r'%3A',url)
    with requests.Session() as s:
        crawl_report = s.get(url)
        content_type = crawl_report.headers['content-type']
        if content_type == 'application/zip':
            output = open(job_dir + '/zips/' + report_type + '-' + host + '.zip','wb')
            output.write(crawl_report.content)
            output.close()
        elif content_type.startswith('text/plain'):
            output = open(job_dir + '/crawled_queued/' + report_type + '-' + host + '.txt','w')
            output.write(crawl_report.content)
            output.close()

def extract_reports(job_dir):
    print "Extracting zips"
    zip_dir = join(job_dir,'zips')
    extract_dir = join(job_dir, 'crawled_queued')
    for source_zip in os.listdir(zip_dir):
        with zipfile.ZipFile(join(zip_dir,source_zip)) as zf:
            zf.extractall(extract_dir)

def find_repeat_dirs(job_dir, host_list):
    print "Looking for repeating directories"
    repeated_dirs = re.compile(r'^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$')
    repeat_dict = {}
    crawl_txts = join(job_dir,'crawled_queued')
    for filename in os.listdir(crawl_txts):
        host = [host for host in host_list if host in filename]
        host = max(host, key=len)
        report = open(join(crawl_txts,filename)).read()
        for url in report.splitlines():
            if repeated_dirs.match(url):
                if host not in repeat_dict:
                    repeat_dict[host] = {}
                    repeat_dict[host]['count'] = 1
                    repeat_dict[host]['repeats'] = []
                    repeat_dict[host]['repeats'].append(url)
                elif host in repeat_dict:
                    repeat_dict[host]['count'] += 1
                    repeat_dict[host]['repeats'].append(url)
    return repeat_dict

def check_repeat_url_status(repeat_dict):
    print "Checking the status of a random sample of repeating directory URLs"
    for host in repeat_dict:
        print "Checking statuses for {0}".format(host)
        urls = repeat_dict[host]['repeats']
        repeat_dict[host]['ok'] = []
        repeat_dict[host]['maybe'] = []
        repeat_dict[host]['notok'] = []
        repeat_checked = 0
        while (len(urls) > 0) and (repeat_checked < 50):
            url = random.choice(urls)
            urls.remove(url)
            try:
                with requests.Session() as s:
                    repeat_check = s.get(url, headers={'User-Agent':'BHL Archive-It QA'})
                    if repeat_check.status_code == 200 and len(repeat_check.history) == 0:
                        repeat_dict[host]['ok'].append(url)
                    elif repeat_check.status_code == 200 and len(repeat_check.history) > 0:
                        repeat_dict[host]['maybe'].append(url)
                    else:
                        repeat_dict[host]['notok'].append(url)
                repeat_checked += 1
            except:
                continue
    return repeat_dict

def process_repeats(job_dir, repeat_dict):
    print "Processing repeating URLs and writing txt and csv reports"
    repeat_dir_all = join(job_dir,'repeating_directories_all')
    repeat_dir_checked = join(job_dir,'repeating_directories_checked')
    repeat_csv = join(job_dir,'repeating_directories.csv')
    with open(repeat_csv,'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host','Count','OK','Maybe','Not OK'])
    for host in repeat_dict:
        count = repeat_dict[host]['count']
        urls = repeat_dict[host]['repeats']
        ok = len(repeat_dict[host]['ok'])
        maybe = len(repeat_dict[host]['maybe'])
        notok = len(repeat_dict[host]['notok'])
        with open(join(repeat_dir_all, host + '.txt'),'a') as repeat_txt:
            repeat_txt.write('\n'.join(urls))
        with open(repeat_csv,'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([host,count,ok,maybe,notok])
        if ok > 0:
            ok_dir = join(repeat_dir_checked,'ok')
            ok_list = repeat_dict[host]['ok']
            if not os.path.exists(ok_dir):
                os.makedirs(ok_dir)
            with open(join(ok_dir,host + '.txt'),'a') as ok_txt:
                ok_txt.write('\n'.join(ok_list))
        if maybe > 0:
            maybe_dir = join(repeat_dir_checked,'maybe')
            maybe_list = repeat_dict[host]['maybe']
            if not os.path.exists(maybe_dir):
                os.makedirs(maybe_dir)
            with open(join(maybe_dir,host + '.txt'),'a') as maybe_txt:
                maybe_txt.write('\n'.join(maybe_list))
        if notok > 0:
            notok_dir = join(repeat_dir_checked,'notok')
            notok_list = repeat_dict[host]['notok']
            if not os.path.exists(notok_dir):
                os.makedirs(notok_dir)
            with open(join(notok_dir,host + '.txt'),'a') as notok_txt:
                notok_txt.write('\n'.join(notok_list))

def get_seed_source(job_dir):
    source_csv = join(job_dir,'seedsource.csv')
    source_list = []
    with open(source_csv,'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        next(reader,None)
        for row in reader:
            source = row[0]
            if source not in source_list:
                source_list.append(source)
    return source_list

def check_seed_status(job_dir):
    print "Checking seed status reports"
    statuses = {'redirects':{},'robots':{},'unknown':{},'ok':{}}
    status_dir = join(job_dir,'statuses')
    with open(join(job_dir,'seedstatus.csv'),'rb') as status_csv:
        reader = csv.reader(status_csv)
        next(reader,None)
        next(reader,None)
        for row in reader:
            status = row[0]
            url = row[1]
            code = row[2]
            redirect = row[3]
            if code != '200':
                if code == '301' or code == '302':
                    statuses['redirects'][url] = redirect
                elif code == '-9998':
                    statuses['robots'][url] = code
                else:
                    statuses['unknown'][url] = code
            else:
                statuses['ok'][url] = code
    for status in statuses:
        status_csv = join(status_dir, status + '.csv')
        with open(status_csv,'ab') as status_csv:
            writer = csv.writer(status_csv)
            for url in statuses[status]:
                writer.writerow([url, statuses[status][url]])
    return statuses

def get_redirect_metadata(job_dir, source_list, seed_status_dict):
    print "Getting metadata for redirected seeds"
    with open(join(job_dir,'seedstatus.csv'),'rb') as csvfile:
        reader = csv.reader(csvfile)
        first_row = reader.next()
        collection_string = first_row[0]
        collection_id = re.findall(r'(\d+)\t',collection_string)[0]
    starting_seeds = {}
    skip = ['createdDate','lastUpdatedDate','active','public','note','url']
    reconciled = False
    while not reconciled:
        unreconciled_count = 0
        for url in seed_status_dict['redirects']:
            value = seed_status_dict['redirects'][url]
            if (url in source_list) and (value in seed_status_dict['redirects']):
                unreconciled_count += 1
                seed_status_dict['redirects'][url] = seed_status_dict['redirects'][value]
        if unreconciled_count == 0:
            reconciled = True
    for url in seed_status_dict['redirects']:
        if url in source_list:
            starting_seeds[url] = ''
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
    for seed in starting_seeds:
        new_seed = seed_status_dict['redirects'][seed]
        add_seeds.append(new_seed)
        seed_metadata = {}
        seed_path = starting_seeds[seed]
        seed_element = tree.xpath(seed_path)[0]
        for elem in seed_element.xpath('.//*'):
            if elem.text is not None and not elem.tag in skip and not 'name' in elem.attrib:
                elem_name = elem.tag
                elem_text = elem.text
                if elem_name not in seed_metadata:
                    seed_metadata[elem_name] = []
                seed_metadata[elem_name].append(elem_text)
            elif 'name' in elem.attrib:
                if elem.attrib['name'] not in skip:
                    elem_name = elem.attrib['name']
                    elem_text = elem.text
                    if elem_name not in seed_metadata:
                        seed_metadata[elem_name] = []
                    seed_metadata[elem_name].append(elem_text)
        seed_metadata['url'] = []
        seed_metadata['url'].append(new_seed)
        seed_metadata['Note'] = []
        seed_metadata['Note'].append("Seed created due to redirect from " + seed)
        redirect_metadata.append(seed_metadata)
    with open(job_dir,'deactivate.txt','a') as deactivate_txt:
        deactivate_txt.write('\n'.join([seed for seed in starting_seeds]))
    with open(job_dir, 'addseeds.txt','a') as add_seeds_txt:
        add_seeds_txt.write('\n'.join([seed for seed in add_seeds]))
    return redirect_metadata

def process_redirect_metadata(job_dir, redirect_metadata):
    print "Writing CSV with metadata for new seeds"
    header_order = ['url','Title','Subject','Personal Creator','Corporate Creator','Coverage','Description','Publisher','Note']
    redirect_csv = join(job_dir,'redirect_metadata.csv')
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


def build_report_summary():
    pass

def main():
    job = raw_input('Enter a job number: ')
    base_dir = raw_input('Enter a base directory: ')
    job_dir = make_directories(base_dir, job)
    job_dir = join(base_dir,job)
    get_base_reports(job, job_dir)
    host_dict, host_list = get_host_info(job_dir)
    for host in host_dict:
        if (host_dict[host]['crawled'] > 25) or (host_dict[host]['data'] > 1000000000):
            get_crawl_reports(job_dir, job, host, 'crawled')
        if host_dict[host]['queued'] > 0:
            get_crawl_reports(job_dir, job, host, 'queued')
    extract_reports(job_dir)
    repeat_dict = find_repeat_dirs(job_dir, host_list)
    url_status_dict = check_repeat_url_status(repeat_dict)
    process_repeats(job_dir, url_status_dict)
    seed_status_dict = check_seed_status(job_dir)
    source_list = get_seed_source(job_dir)
    redirect_metadata = get_redirect_metadata(job_dir, source_list, seed_status_dict)
    process_redirect_metadata(job_dir, redirect_metadata)
    #build_report_summary()
    print "All done! Find completed reports at {0}".format(job_dir)


main()
