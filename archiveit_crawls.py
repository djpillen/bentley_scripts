import requests
import csv
import re
import os
from os.path import join
import zipfile

#https://partner.archive-it.org/seam/resource/crawledByHost?crawlJobId=173627&host=mgoblog.com
#https://partner.archive-it.org/seam/resource/queuedByHost?crawlJobId=173627&host=mgoblog.com

crawl_reports = 'U:/web_archives/test_crawls/'
host_reports = 'U:/web_archives/test_crawls/hosts/'

def main():
    for filename in os.listdir(host_reports):
        collection = filename.replace('.csv','')
        print "Downloading reports for {0}".format(collection)
        report = host_reports + filename
        job = get_job_id(report)
        hosts = get_hosts(report)
        for host in hosts:
            if hosts[host]['crawled'] > 100:
                get_crawl_reports(collection, job, host, 'crawled')
            if hosts[host]['queued'] > 0:
                get_crawl_reports(collection, job, host, 'queued')
        extract_reports(collection)


# read the host report to find JobId
def get_job_id(report):
    with open(report,'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        next(reader,None)
        found = False
        while found is False:
            for row in reader:
                if len(row[10]) > 0:
                    job = re.findall(r'JobId\=(\d+)',row[10])
                    found = True
        return job[0]

def get_reports(job):
    pass
    # get the host and seed status reports

# read the host report to get a dict of hosts and their crawled and queued counts
def get_hosts(report):
    with open(report,'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        next(reader,None)
        hosts = {}
        for row in reader:
            host = row[0]
            crawled = row[1]
            queued = row[6]
            hosts[host] = {}
            hosts[host]['crawled'] = int(crawled)
            hosts[host]['queued'] = int(queued)
        return hosts

# download crawled and queued reports
def get_crawl_reports(collection, job, host, report_type):
    url = 'https://partner.archive-it.org/seam/resource/' + report_type + 'ByHost?crawlJobId=' + job + '&host=' + host
    if url.endswith(':'):
        re.sub(r':$',r'%3A',url)
    collection_dir = crawl_reports + collection
    request = requests.get(url)
    content_type = request.headers['content-type']
    if content_type == 'application/zip':
        if not os.path.exists(collection_dir + '/zips'):
            os.makedirs(collection_dir + '/zips')
        output = open(collection_dir + '/zips/' + report_type + '-' + host + '.zip','wb')
        output.write(request.content)
        output.close()
    elif content_type.startswith('text/plain'):
        if not os.path.exists(collection_dir + '/extracted'):
            os.makedirs(collection_dir + '/extracted')
        output = open(collection_dir + '/extracted/' + report_type + '-' + host + '.txt','w')
        output.write(request.content)
        output.close()

# extract downloaded zips
def extract_reports(collection):
    print "Extracting zips for {0}".format(collection)
    zip_dir = crawl_reports + collection + '/zips'
    extract_dir = crawl_reports + collection + '/extracted'
    if os.path.exists(zip_dir):
        for source_zip in os.listdir(zip_dir):
            with zipfile.ZipFile(join(zip_dir,source_zip)) as zf:
                zf.extractall(extract_dir)

main()
#read reports line by line
# report = open(report_path,'r').read()
#for line in report.splitlines():
    #do something with line
