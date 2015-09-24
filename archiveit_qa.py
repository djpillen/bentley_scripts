import requests
import csv
import re
import os
from os.path import join
import zipfile

def make_dirs(base_dir, job):
    print "Making directories"
    job_dir = join(base_dir,job)
    os.makedirs(job_dir)
    os.makedirs(join(job_dir,'zips'))
    os.makedirs(join(job_dir,'crawled_queued'))
    os.makedirs(join(job_dir,'repeating_directories'))
    return job_dir

def get_base_reports(job, job_dir):
    print "Getting host and seed reports"
    hosts_report = requests.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=host')
    with open(join(job_dir,'hosts.csv'),'wb') as host_csv:
        host_csv.write(hosts_report.content)
    status_report = requests.get('https://partner.archive-it.org/seam/resource/report?crawlJobId=' + job + '&type=seed')
    with open(join(job_dir,'seedstatus.csv'),'wb') as status_csv:
        status_csv.write(status_report.content)
    
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
            queued = row[6]
            host_dict[host] = {}
            host_dict[host]['crawled'] = int(crawled)
            host_dict[host]['queued'] = int(queued)
            if host.endswith(':'):
                host = re.sub(r':$','',host)
            host_list.append(host)
    return host_dict, host_list

def get_crawl_reports(job_dir, job, host, report_type):
    print "Getting {0} reports for {1}".format(report_type, host)
    url = 'https://partner.archive-it.org/seam/resource/' + report_type + 'ByHost?crawlJobId=' + job + '&host=' + host
    if url.endswith(':'):
        re.sub(r':$',r'%3A',url)
    crawl_report = requests.get(url)
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
    zip_dir = job_dir + '/zips'
    extract_dir = job_dir + '/crawled_queued'
    if os.path.exists(zip_dir):
        for source_zip in os.listdir(zip_dir):
            with zipfile.ZipFile(join(zip_dir,source_zip)) as zf:
                zf.extractall(extract_dir)
                
def find_repeat_dirs(job_dir, host_list):
    print "Looking for repeating directories"
    repeated_dirs = re.compile(r'^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$')
    repeat_dict = {}
    crawl_txts = join(job_dir,'crawled_queued')
    for filename in os.listdir(crawl_txts):
        host = host = [host for host in host_list if host in filename]
        host = max(host, key=len)
        report = report = open(join(crawl_txts,filename)).read()
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

def process_repeats(job_dir, repeat_dict):
    print "Processing repeating directories"
    repeat_dir = join(job_dir,'repeating_directories')
    repeat_csv = join(job_dir,'repeating_directories.csv')
    with open(repeat_csv,'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host','Count','OK'])
    for host in repeat_dict:
        count = repeat_dict[host]['count']
    
        #OK = 0
        #NotOK = 0
        for url in repeat_dict[host]['repeats']:
            with open(join(repeat_dir, host + '.txt'),'a') as repeat_txt:
                repeat_txt.write(url + '\n')
        """
            with requests.Session() as s:
                repeat_check = s.get(url)
                if repeat_check.status_code == '200':
                    OK += 1
                else:
                    NotOK += 1
        """
        with open(repeat_csv,'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([host,count])
    
def main():
    job = raw_input('Enter a job number: ')
    base_dir = raw_input('Enter a base directory: ')
    job_dir = make_dirs(base_dir, job)
    get_base_reports(job, job_dir)
    host_dict, host_list = get_host_info(job_dir)
    for host in host_dict:
        if host_dict[host]['crawled'] > 0:
            get_crawl_reports(job_dir, job, host, 'crawled')
        if host_dict[host]['queued'] > 0:
            get_crawl_reports(job_dir, job, host, 'queued')
    extract_reports(job_dir)
    repeat_dict = find_repeat_dirs(job_dir, host_list)
    process_repeats(job_dir, repeat_dict)
    print "All done! Find completed reports at {0}".format(job_dir)
    
    
main()
    
    