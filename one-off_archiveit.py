import csv
import re
import os
from os.path import join

host_reports = 'U:/web_archives/test_crawls/hosts'
base_dir = 'U:/web_archives/test_crawls'

for filename in os.listdir(host_reports):
    print "Processing repeat directories for {0}".format(filename)
    collection = filename.replace('.csv','')
    collection_dir = join(base_dir,collection)
    repeat_dir = join(collection_dir,'repeating_directories')
    if not os.path.exists(repeat_dir):
        os.makedirs(repeat_dir)
    extracted = join(collection_dir, 'extracted')
    host_list = []
    repeat_dict = {}
    print "Building host list"
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
                    host = re.sub(r':$','',host)
                if host not in host_list:
                    host_list.append(host)
    print "Checking urls"
    for filename in os.listdir(extracted):
        repeated_dirs = re.compile(r'^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$')
        host = [host for host in host_list if host in filename]
        if len(host) < 1:
            print filename
        host = max(host, key=len)
        report = open(join(extracted,filename)).read()
        for url in report.splitlines():
            if repeated_dirs.match(url):
                if host not in repeat_dict:
                    repeat_dict[host] = []
                    repeat_dict[host].append(url)
                elif host in repeat_dict:
                    repeat_dict[host].append(url)
    print "Writing files"
    for host in repeat_dict:
        urls = repeat_dict[host]
        with open(join(repeat_dir, host + '.txt'),'a') as repeat_txt:
            repeat_txt.write('\n'.join(urls))
