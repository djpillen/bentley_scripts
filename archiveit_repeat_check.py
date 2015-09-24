import requests
import random
import csv
import os
from os.path import join

base_dir = 'U:/web_archives/test_crawls'
collections = ['admin','alumni','athletics','schools','studentorgs','mhc','health','news']

for collection in collections:
    print "Evaluating repeating directories for {0}".format(collection)
    hosts = {}
    collection_dir = join(base_dir,collection)
    repeat_checked_dir = join(collection_dir,'repeating_checked')
    if not os.path.exists(repeat_checked_dir):
        os.makedirs(repeat_checked_dir)
    repeat_dir = join(collection_dir,'repeating_directories')
    repeat_csv = join(collection_dir,'repeating_directories.csv')
    if os.path.exists(repeat_csv):
        os.remove(repeat_csv)
    with open(repeat_csv,'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Host','Count','OK','Maybe','Not OK'])
    for filename in os.listdir(repeat_dir):
        hosts[filename] = {}
        hosts[filename]['repeats'] = []
        repeat_txt =  open(join(repeat_dir,filename)).read()
        for url in repeat_txt.splitlines():
            hosts[filename]['repeats'].append(url)
    for host in hosts:
        print "Checking status codes for repeat directories in {0}".format(host)
        urls = hosts[host]['repeats']
        hosts[host]['count'] = len(urls)
        hosts[host]['ok'] = []
        hosts[host]['maybe'] = []
        hosts[host]['notok'] = []
        repeat_checked = 0
        while (len(urls) > 0) and (repeat_checked < 50):
            url = random.choice(urls)
            urls.remove(url)
            try:
                with requests.Session() as s:
                    repeat_check = s.get(url)
                    if repeat_check.status_code == 200 and len(repeat_check.history) == 0:
                        hosts[host]['ok'].append(url)
                    elif repeat_check.status_code == 200 and len(repeat_check.history) > 0:
                        hosts[host]['maybe'].append(url)
                    else:
                        hosts[host]['notok'].append(url)
                repeat_checked += 1
            except:
                continue
    for host in hosts:
        print "Building documents for {0}".format(host)
        count = hosts[host]['count']
        ok = len(hosts[host]['ok'])
        maybe = len(hosts[host]['maybe'])
        notok = len(hosts[host]['notok'])
        with open(repeat_csv,'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([host,count,ok,maybe,notok])
        if ok > 0:
            ok_dir = join(repeat_checked_dir,'ok')
            if not os.path.exists(ok_dir):
                os.makedirs(ok_dir)
            for url in hosts[host]['ok']:
                with open(join(okay_dir,host),'a') as ok_txt:
                    ok_txt.write(url + '\n')
        if maybe > 0:
            maybe_dir = join(repeat_checked_dir,'maybe')
            if not os.path.exists(maybe_dir):
                os.makedirs(maybe_dir)
            for url in hosts[host]['maybe']:
                with open(join(maybe_dir,host),'a') as maybe_txt:
                    maybe_txt.write(url + '\n')
        if notok > 0:
            notok_dir = join(repeat_checked_dir,'notok')
            if not os.path.exists(notok_dir):
                os.makedirs(notok_dir)
            for url in hosts[host]['notok']:
                with open(join(notok_dir,host),'a') as notok_txt:
                    notok_txt.write(url + '\n')
