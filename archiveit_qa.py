import csv
import HTMLParser
from lxml import etree
import os
from os.path import join
import random
import re
import requests
import time
import urlparse
import zipfile

def make_directories(base_dir, job):
    job_dir = join(base_dir,job)
    os.makedirs(job_dir)
    os.makedirs(join(job_dir,'crawled_queued'))
    os.makedirs(join(job_dir,'statuses'))

def get_base_reports(job, job_dir):
    session = requests.session()
    with requests.session() as session:
        session.headers["User-Agent"] = "BHL Archive-It QA"
        hosts_report = session.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=host')
        with open(join(job_dir,'hosts.csv'),'wb') as host_csv:
            host_csv.write(hosts_report.content)
        status_report = session.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=seed')
        with open(join(job_dir,'seedstatus.csv'),'wb') as status_csv:
            status_csv.write(status_report.content)
        source_report = session.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=source')
        with open(join(job_dir,'seedsource.csv'),'wb') as source_csv:
            source_csv.write(source_report.content)

def get_host_info(job_dir):
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
        s.headers["User-Agent"] = "BHL Archive-It QA"
        crawl_report = s.get(url)
        content_type = crawl_report.headers['content-type']
        if content_type == 'application/zip':
            if not os.path.exists(join(job_dir,'zips')):
                os.makedirs(join(job_dir,'zips'))
            output = join(job_dir, "zips", "{0}-{1}.zip".format(report_type, host))
            with open(output, "wb") as f:
                f.write(crawl_report.content)
        elif content_type.startswith('text/plain'):
            output = join(job_dir, "crawled_queued", "{0}-{1}.txt".format(report_type, host))
            with open(output, "w") as f:
                f.write(crawl_report.content)
    time.sleep(1)

def extract_reports(job_dir):
    zip_dir = join(job_dir,'zips')
    extract_dir = join(job_dir, 'crawled_queued')
    for source_zip in os.listdir(zip_dir):
        with zipfile.ZipFile(join(zip_dir,source_zip)) as zf:
            zf.extractall(extract_dir)

def find_repeat_dirs(job_dir, host_list):
    repeated_dirs = re.compile(r'^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$')
    repeat_dict = {}
    crawl_txts = join(job_dir,'crawled_queued')
    for filename in os.listdir(crawl_txts):
        host = [host for host in host_list if host in filename]
        host = max(host, key=len)
        with open(join(crawl_txts, filename)) as f:
            report = f.read()
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
    if len(repeat_dict) > 0:
        repeat_dir = join(job_dir,'repeating_directories')
        if not os.path.exists(repeat_dir):
            os.makedirs(repeat_dir)
        repeat_dir_all = join(repeat_dir,'all')
        os.makedirs(repeat_dir_all)
        for host in repeat_dict:
            urls = repeat_dict[host]['repeats']
            with open(join(repeat_dir_all, host + '.txt'),'w') as repeat_txt:
                repeat_txt.write('\n'.join(urls))
        return repeat_dict
    else:
        return False

def check_repeat_url_status(repeat_dict):
    for host in repeat_dict:
        print "Checking statuses for {0}".format(host)
        urls = [url for url in repeat_dict[host]['repeats']]
        repeat_dict[host]['ok'] = []
        repeat_dict[host]['maybe'] = []
        repeat_dict[host]['notok'] = []
        repeat_checked = 0
        while (len(urls) > 0) and (repeat_checked < 50):
            url = random.choice(urls)
            urls.remove(url)
            try:
                with requests.Session() as s:
                    s.headers["User-Agent"] = "BHL Archive-It QA"
                    repeat_check = s.head(url)
                    if repeat_check.status_code == 200 and len(repeat_check.history) == 0:
                        repeat_dict[host]['ok'].append(url)
                    elif repeat_check.status_code == 200 and len(repeat_check.history) > 0:
                        repeat_dict[host]['maybe'].append(url)
                    else:
                        repeat_dict[host]['notok'].append(url)
                repeat_checked += 1
                time.sleep(2)
            except:
                continue
    return repeat_dict

def process_repeats(job_dir, repeat_dict):
    repeat_dir = join(job_dir,'repeating_directories')
    repeat_csv = join(repeat_dir,'repeating_directories.csv')

    repeat_csv_data = []
    for host in repeat_dict:
        count = repeat_dict[host]['count']
        ok = len(repeat_dict[host]['ok'])
        maybe = len(repeat_dict[host]['maybe'])
        notok = len(repeat_dict[host]['notok'])
        repeat_csv_data.append([host, count, ok, maybe, notok])
        if ok > 0:
            ok_dir = join(repeat_dir,'ok')
            ok_list = repeat_dict[host]['ok']
            if not os.path.exists(ok_dir):
                os.makedirs(ok_dir)
            with open(join(ok_dir,host + '.txt'),'a') as ok_txt:
                ok_txt.write('\n'.join(ok_list))
        if maybe > 0:
            maybe_dir = join(repeat_dir,'maybe')
            maybe_list = repeat_dict[host]['maybe']
            if not os.path.exists(maybe_dir):
                os.makedirs(maybe_dir)
            with open(join(maybe_dir,host + '.txt'),'a') as maybe_txt:
                maybe_txt.write('\n'.join(maybe_list))
        if notok > 0:
            notok_dir = join(repeat_dir,'notok')
            notok_list = repeat_dict[host]['notok']
            if not os.path.exists(notok_dir):
                os.makedirs(notok_dir)
            with open(join(notok_dir,host + '.txt'),'a') as notok_txt:
                notok_txt.write('\n'.join(notok_list))

    with open(repeat_csv, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(['Host','Count','OK','Maybe','Not OK'])
        writer.writerows(repeat_csv_data)

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
        status_data = []
        for url in statuses[status]:
            status_data.append([url, statuses[status][url]])
        with open(status_csv, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(status_data)

    return statuses

def minimal_redirect_handling(job_dir, source_list, seed_status_dict):
    redirect_dir = join(job_dir,'redirects')
    starting_seeds = {}
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
            redirect_url = seed_status_dict['redirects'][url]
            seed_parse = urlparse.urlparse(url)
            redirect_parse = urlparse.urlparse(redirect_url)
            # Check to see if the starting URL and redirected URL are meaningfully different
            if ((seed_parse.path != redirect_parse.path) and ((seed_parse.path + '/' != redirect_parse.path) and (seed_parse.path != redirect_parse.path + '/'))) or ((seed_parse.netloc != redirect_parse.netloc) and (('www.' + seed_parse.netloc != redirect_parse.netloc) and (seed_parse.netloc != 'www.' + redirect_parse.netloc))) or (seed_parse.params != redirect_parse.params) or (seed_parse.query != redirect_parse.query) or (seed_parse.fragment != redirect_parse.fragment):
                starting_seeds[url] = redirect_url

    redirect_data = []
    for seed, redirect in starting_seeds.items():
        redirect_data.append([seed, redirect, ''])

    with open(join(redirect_dir,'redirect_information.csv'),'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Seed URL','Redirect URL','Notes'])
        writer.writerows(redirect_data)

def get_redirect_metadata(job_dir, source_list, seed_status_dict):
    redirect_dir = join(job_dir,'redirects')
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
            redirect_url = seed_status_dict['redirects'][url]
            seed_parse = urlparse.urlparse(url)
            redirect_parse = urlparse.urlparse(redirect_url)
            # Check to see if the starting URL and redirected URL are meaningfully different
            if ((seed_parse.path != redirect_parse.path) and ((seed_parse.path + '/' != redirect_parse.path) and (seed_parse.path != redirect_parse.path + '/'))) or ((seed_parse.netloc != redirect_parse.netloc) and (('www.' + seed_parse.netloc != redirect_parse.netloc) and (seed_parse.netloc != 'www.' + redirect_parse.netloc))) or (seed_parse.params != redirect_parse.params) or (seed_parse.query != redirect_parse.query) or (seed_parse.fragment != redirect_parse.fragment):
                starting_seeds[url] = ''
    with requests.Session() as s:
        s.headers["User-Agent"] = "BHL Archive-It QA"
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
    redirect_investigate = []
    entity_parser = HTMLParser.HTMLParser()
    for seed in starting_seeds:
        if len(starting_seeds[seed]) > 0:
            new_seed = seed_status_dict['redirects'][seed]
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
            seed_metadata['Note'].append("QA Note: This seed was created as a result of the previous seed URL redirecting to this URL. Previous captures under seed URL " + seed)
            redirect_metadata.append(seed_metadata)
        else:
            redirect_investigate.append(seed)

    add_and_deactivate_data = []
    for seed, new_seed in add_deactivate.items():
        add_and_deactivate_data.append([new_seed, seed, 'QA NOTE: Seed URL redirects to ' + new_seed + '. A new seed with the redirected seed URL has been added.',''])
    
    with open(join(redirect_dir,'add_and_deactivate.csv'),'wb') as add_deactivate_csv:
        writer = csv.writer(add_deactive_csv)
        writer.writerow(['Add','Deactivate','Deactivation Note','Notes'])
        writer.writerows(add_and_deactivate_data)
    
    with open(join(redirect_dir,'redirect_investigate.txt'),'a') as investigate_txt:
        investigate_txt.write('\n'.join([seed for seed in redirect_investigate]))
    return redirect_metadata

def process_redirect_metadata(job_dir, redirect_metadata):
    header_order = ['url','Title','Subject','Personal Creator','Corporate Creator','Coverage','Description','Publisher','Note']
    redirect_dir = join(job_dir,'redirects')
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


    redirect_csv_data = []
    for seed in redirect_metadata:
        row = []
        for element in header_order:
            elem_lower = element.lower()
            if element in seed:
                row.extend([item for item in seed[element]])
            elif elem_lower in seed:
                row.extend([item for item in seed[elem_lower]])
        redirect_csv_data.append(row)

    with open(redirect_csv,'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(head_row)
        writer.writerows(redirect_csv_data)


def main():
    job_numbers = raw_input('Enter a comma separated list of job numbers: ')
    base_dir = raw_input('Enter a directory to save job files (e.g., U:/web_archives/jobs): ')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    jobs = [job.strip() for job in job_numbers.split(',')]
    for job in jobs:
        print "Making necessary directories for job {0}".format(job)
        make_directories(base_dir, job)
        job_dir = join(base_dir,job)
        print "Getting host and seed reports for job {0}".format(job)
        get_base_reports(job, job_dir)
        print "Building a dictionary and list of hosts for job {0}".format(job)
        host_dict, host_list = get_host_info(job_dir)
        source_list = get_seed_source(job_dir)
        for host in host_dict:
            if (host_dict[host]['crawled'] > 25) or (host_dict[host]['data'] > 1000000000):
                get_crawl_reports(job_dir, job, host, 'crawled')
            if host_dict[host]['queued'] > 0:
                get_crawl_reports(job_dir, job, host, 'queued')
        if os.path.exists(join(job_dir,'zips')):
            print "Extracting zips for job {0}".format(job)
            extract_reports(job_dir)
        print "Looking for repeating directories for job {0}".format(job)
        repeat_dict = find_repeat_dirs(job_dir, host_list)
        if repeat_dict:
            print "Repeating directories found! Checking the status of a random sample of repeating URLs for job {0}".format(job)
            url_status_dict = check_repeat_url_status(repeat_dict)
            print "Processing repeating URLs and writing txt and csv reports for job {0}".format(job)
            process_repeats(job_dir, url_status_dict)
        else:
            print "No repeating directories found for job {0}".format(job)
        print "Checking seed status reports for job {0}".format(job)
        seed_status_dict = check_seed_status(job_dir)
        if len(seed_status_dict['redirects']) > 0:
            if not os.path.exists(join(job_dir,'redirects')):
                os.makedirs(join(job_dir,'redirects'))
            print "Redirected seeds found! Getting metadata for redirected seeds for job {0}".format(job)
            minimal_redirect_handling(job_dir, source_list, seed_status_dict)
            # Trying to do this with another script, archiveit_redirect.py, the idea being that this qa script can give you a list of
            # seed URLs that redirect and that list can be checked before actually fetching the redirect metadata and building the final
            # list of seeds to be deactivated and added
            #redirect_metadata = get_redirect_metadata(job_dir, source_list, seed_status_dict)
            #print "Writing CSV with metadata for new seeds for job {0}".format(job)
            #process_redirect_metadata(job_dir, redirect_metadata)
        else:
            print "No redirected seeds found for job {0}".format(job)
        print "All done! Find completed reports at {0}".format(job_dir)

main()
