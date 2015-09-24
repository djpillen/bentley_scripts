import csv
import os
from os.path import join

base_dir = 'U:/web_archives/test_crawls'
seed_reports = 'U:/web_archives/test_crawls/seed_status'

for filename in os.listdir(seed_reports):
    collection = filename.replace('.csv','')
    collection_dir = join(base_dir,collection)
    status_dir = join(collection_dir,'statuses')
    if not os.path.exists(status_dir):
        os.makedirs(status_dir)
    statuses = {'redirects':{},'robots':{},'unknown':{}}
    with open(join(seed_reports,filename)) as status_csv:
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
    for status in statuses:
        status_csv = join(status_dir, status + '.csv')
        if os.path.exists(status_csv):
            os.remove(status_csv)
        with open(status_csv,'ab') as status_csv:
            writer = csv.writer(status_csv)
            for url in statuses[status]:
                writer.writerow([url, statuses[status][url]])
