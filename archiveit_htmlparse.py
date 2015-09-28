import csv
import HTMLParser
import os
from os.path import join

entity_parser = HTMLParser.HTMLParser()

jobs_dir = 'U:/web_archives/jobs'

for job in os.listdir(jobs_dir):
    job_dir = join(jobs_dir,job)
    redirect_dir = join(job_dir,'redirects')
    starting = open(join(reditect_dir,'redirect_metadata.csv'),'rb')
    the_data = starting.read()
    starting.close()
    unescaped = entity_parser.unescape(the_data)
    fixed = open(join(redirect_dir,'redirect_metadata_fixed.csv'),'wb')
    fixed.write(unescaped)
    fixed.close()
