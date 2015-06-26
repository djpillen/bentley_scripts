import lxml
from lxml import etree
import csv
import docx
from docx import Document
import re
import os
from os.path import join

path = 'Real_Masters_all'

title_file = 'collection_titles.csv'
top_level_file = 'accessrestrict_toplevel-3.csv'
expired_file = 'accessrestrict_expired_fulltext.csv'
all_dates_file = 'accessrestrictdate-7.csv'
no_date_file = 'accessrestrict-nodate.csv'

access_restrictions = {}
current_dict = {}
non_time = {}

with open(expired_file, 'rb') as expired_csv:
    reader = csv.reader(expired_csv)
    next(reader, None)
    for row in reader:
        filename = row[0]
        date_path = row[1]
        expiration_date = row[2]
        full_text = row[3]
        full_text = re.sub('\<\/?(.*?)\>','', full_text)
        full_text = full_text
        if filename not in access_restrictions:
            access_restrictions[filename] = {}
        if 'Expired' not in access_restrictions[filename]:
            access_restrictions[filename]['Expired'] = {}

        access_restrictions[filename]['Expired'][date_path] = {}
        access_restrictions[filename]['Expired'][date_path]['Expiration_date'] = expiration_date
        access_restrictions[filename]['Expired'][date_path]['Full_text'] = full_text
        
        component_path = re.sub('\/accessrestrict\/p\/date','',date_path)
        component_path = component_path
        tree = etree.parse(join(path,filename))
        for r in tree.xpath(component_path):
            try:
                container = r.xpath('.//container')
                box_number = container[0].text
                access_restrictions[filename]['Expired'][date_path]['Container_number'] = box_number
            except:
                access_restrictions[filename]['Expired'][date_path]['Container_number'] = 'N/A'
                
with open(title_file,'rb')as titles_csv:
    reader = csv.reader(titles_csv)
    next(reader, None)
    for row in reader:
        filename = row[0]
        coll_title = row[1]
        if filename in access_restrictions:
            access_restrictions[filename]['Title'] = coll_title
            
            
with open(top_level_file, 'rb') as top_csv:
    reader = csv.reader(top_csv)
    for row in reader:
        filename = row[0]
        restriction = row[2]
        restriction = restriction.replace('<item>','\n')
        restriction = re.sub('\<\/?(.*?)\>','', restriction)
        restriction = restriction
        if filename in access_restrictions:
            access_restrictions[filename]['Restriction'] = restriction
            
with open(all_dates_file,'rb') as all_csv:
    reader = csv.reader(all_csv)
    for row in reader:
        filename = row[0]
        normal = row[3]
        if normal > '2015-07-02':
            if filename not in current_dict:
                current_dict[filename] = 1
            else:
                current_dict[filename] += 1

                
with open(no_date_file, 'rb') as no_date_csv:
    reader = csv.reader(no_date_csv)
    for row in reader:
        filename = row[0]
        if filename not in non_time:
            non_time[filename] = 1
        else:
            non_time[filename] += 1
            


for filename in access_restrictions:
    if filename in current_dict:
        access_restrictions[filename]['Remaining_time'] = str(current_dict[filename])
    else:
        access_restrictions[filename]['Remaining_time'] = '0'
        
    if filename in non_time:
        access_restrictions[filename]['Remaining_non_time'] = str(non_time[filename])
    else:
        access_restrictions[filename]['Remaining_non_time'] = '0'
    
    
document = Document()

for filename in access_restrictions:
    document.add_heading(access_restrictions[filename]['Title'])
    document.add_heading('Collection Level Restriction', level=2)
    document.add_paragraph(access_restrictions[filename]['Restriction'])
    document.add_heading('Expired Restrictions', level=2)
    table = document.add_table(rows=1, cols=3)
    table.autofit = True
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Container"
    hdr_cells[1].text = 'Expiration Date'
    hdr_cells[2].text = 'Full Restriction'
    for date_path in access_restrictions[filename]['Expired']:
        row_cells = table.add_row().cells
        row_cells[0].text = access_restrictions[filename]['Expired'][date_path]['Container_number']
        row_cells[1].text = access_restrictions[filename]['Expired'][date_path]['Expiration_date']
        row_cells[2].text = access_restrictions[filename]['Expired'][date_path]['Full_text']

            
    table.style= "TableGrid"
    document.add_paragraph('Remaining Time-Bound Restrictions')
    document.add_paragraph(access_restrictions[filename]['Remaining_time'])
    document.add_paragraph('Remaining Non-Time-Bound Restrictions')
    document.add_paragraph(access_restrictions[filename]['Remaining_non_time'])
    document.add_page_break()
    
document.save('test.docx')