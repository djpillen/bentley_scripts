from lxml import etree
import os
from os.path import join
import csv
import re



ead = etree.parse('C:/Users/Public/Documents/7.xml')
unitid = ead.xpath("/ead/archdesc/did/unitid")
call_no = unitid[0].text
collection_id = re.compile(r'^\d+')
collection_id = re.findall(collection_id,call_no)[0]
components = ead.xpath("//*[starts-with(local-name(), 'c0')]")

box_num_components = {}

# Check each component for multiple containers
for component in components:
    containers = component.xpath('./did/container')
    unittitle = component.xpath('./did/unittitle')
    unitdate = component.xpath('./did/unitdate')
    if unittitle and unittitle[0].text:
        title = unittitle[0].text.encode('utf-8')
    else:
        title = unitdate[0].text.encode('utf-8')
    if containers:
        ref_id = component.attrib['id']
        ref_id = ref_id.replace('aspace_','')
        box_type_num = containers[0].attrib['type'] + ' ' + containers[0].text
        box_num = containers[0].text.encode('utf-8')
        if box_num not in box_num_components:
            box_num_components[box_num] = 1
        identifier = collection_id+'.'+box_num+'.'+str(box_num_components[box_num])
        box_num_components[box_num] = box_num_components[box_num] + 1
        with open('C:/Users/Public/Documents/7.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow([box_type_num, title, ref_id, identifier])
        print ref_id
