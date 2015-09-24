import os
from os.path import join
import csv
import re
import requests

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
    repeat_csv = 'U:/web_archives/test_crawls/' + collection +'/repeating_directories.csv'
    repeat_dir = 'U:/web_archives/test_crawls/' + collection + '/repeating_directories'
    os.makedirs(repeat_dir)
    
                

    if os.path.exists(repeat_csv):
        os.remove(repeat_csv)

    with open(repeat_csv,'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host','Count','OK','Not OK'])

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
                    hosts[host]['count'] = 1
                    hosts[host]['repeats'] = []
                    hosts[host]['repeats'].append(url)
                elif host in hosts:
                    hosts[host]['count'] += 1
                    hosts[host]['repeats'].append(url)
                

    print "Creating CSV for {0}".format(collection)
    for host in sorted(hosts, key=hosts.get('count'), reverse=True):
        count = hosts[host]['count']
        OK = 0
        NotOK = 0
        for url in hosts[host]['repeats']:
            with open(repeat_dir + '/' + host + '.txt','a') as repeat_txt:
                repeat_txt.write(url + '\n')
            repeat_check = requests.get(url)
            if repeat_check.status_code == '200':
                OK += 1
            else:
                NotOK += 1
        with open(repeat_csv,'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([host,count,OK,NotOK])
                
    





#read reports line by line
# report = open(report_path,'r').read()
#for line in report.splitlines():
    #do something with line
