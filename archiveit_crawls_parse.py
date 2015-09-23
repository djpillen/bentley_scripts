import os
from os.path import join
import csv
import re

repeated_dirs = re.compile(r'^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$')

host_reports = 'U:/web_archives/test_crawls/hosts'

collections = []
host_list = []

for filename in os.listdir(host_reports):
    print "Building list of hosts:", filename
    collections.append(filename.replace('.csv',''))
    with open(join(host_reports,filename),'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        next(reader,None)
        for row in reader:
            crawled = row[1]
            queued = row[6]
            host = row[0]
            if (int(crawled) > 0) or (int(queued) > 0):
                if host.endswith(':'):
                    re.sub(r':$','',host)
                if host not in host_list:
                    host_list.append(host)

for collection in collections:
    hosts = {}
    extracted = 'U:/web_archives/test_crawls/' + collection + '/extracted'
    repeaters = 'U:/web_archives/test_crawls/' + collection +'/repeating_directories.csv'

    if os.path.exists(repeaters):
        os.remove(repeaters)

    with open(repeaters,'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host','Count'])

    print "Searching for repeating directories in", collection
    for filename in os.listdir(extracted):
        host = [host for host in host_list if host in filename]
        if len(host) < 1:
            print filename
        host = max(host, key=len)
        report = open(join(extracted,filename)).read()
        for url in report.splitlines():
            if repeated_dirs.match(url):
                if host not in hosts:
                    hosts[host] = 1
                elif host in hosts:
                    hosts[host] += 1

    print "Creating CSV for {0}".format(collection)
    for host in sorted(hosts, key=hosts.get, reverse=True):
        count = hosts[host]
        with open(repeaters,'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([host,count])






#read reports line by line
# report = open(report_path,'r').read()
#for line in report.splitlines():
    #do something with line
