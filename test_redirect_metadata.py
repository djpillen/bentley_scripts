import csv
import os
from os.path import join

job_dir = 'U:/web_archives/redirects'

redirect_metadata = []
redirect1 = {'url':['www.blah.com'],'Title':['this is my title'],'subject':['cup','phone','pizza'],'personal creator':['Dallas'],'corporate creator':['UM'],'Description':['Test redirect1'],'Publisher':['Scholastic'],'Note':['This is a test of redirect1']}
redirect_metadata.append(redirect1)
redirect2 = {'url':['www.boo.com'],'Coverage':['Detroit'],'Title':['this is my title2'],'subject':['computer'],'corporate creator':['HP'],'Description':['Test redirect2'],'Note':['This is a test of redirect2']}
redirect_metadata.append(redirect2)
redirect3 = {'url':['www.blah.com'],'Coverage':['Ann Arbor'],'subject':['laptop','pin','pencil','paper','phone','eraser'],'personal creator':['John'],'Description':['Test redirect3'],'Publisher':['UM'],'Note':['This is a test of redirect3']}
redirect_metadata.append(redirect3)


redirect_csv = join(job_dir,'redirect_metadata.csv')
header_counts = {}
for seed in redirect_metadata:
    for element in seed:
        count = len(seed[element])
        if element not in header_counts:
            header_counts[element] = count
        elif count > header_counts[element]:
            header_counts[element] = count
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
header_order = ['url','Title','Subject','Personal Creator','Corporate Creator','Coverage','Description','Publisher','Note']
header_row = []
header_counts_lower = {k.lower():v for k,v in header_counts.items()}
for element in header_order:
    elem_lower = element.lower()
    header_row.extend([element] * header_counts_lower[elem_lower])
with open(redirect_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header_row)
for seed in redirect_metadata:
    row = []
    for element in header_order:
        try:
            row.extend([item for item in seed[element]])
        except:
            element = element.lower()
            row.extend([item for item in seed[element]])
    with open(redirect_csv,'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
