import csv
import HTMLParser
import os
from os.path import join

entity_parser = HTMLParser.HTMLParser()

jobs_dir = 'U:/web_archives/jobs'

for job in os.listdir(jobs_dir):
    print job
    job_dir = join(jobs_dir,job)
    redirect_dir = join(job_dir,'redirects')
    if os.path.exists(redirect_dir):
        starting = open(join(redirect_dir,'redirect_metadata.csv'),'rb')
        the_data = starting.read()
        starting.close()
        unescaped = entity_parser.unescape(the_data).encode('utf-8')
        fixed = open(join(redirect_dir,'redirect_metadata_fixed.csv'),'wb')
        fixed.write(unescaped)
        fixed.close()
