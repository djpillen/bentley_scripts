from lxml import etree
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
csv_file = 'C:/Users/Public/Documents/to_investigate/date_to_separate-20150626.csv'

with open(csv_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        filename = row[0]
        print filename
        origin_xpath = row[1]
        origin_text = row[2]
        ead = open(join(path,filename))
        tree = etree.parse(ead)
        for date in tree.xpath(origin_xpath):
            if date.text == origin_text:
                date_parent = date.getparent()
                if 'type' in date.attrib:
                    date_type = date.attrib['type']
                else:
                    date_type = False
                if 'encodinganalog' in date.attrib:
                    date_analog = date.attrib['encodinganalog']
                else:
                    date_analog = False
                origin_index = date_parent.index(date)
                changed_dates = 0
                index = 1
                print date.text
                new_dates = int(raw_input("How many dates?: "))
                while changed_dates < new_dates:
                    new_date = etree.Element("unitdate")
                    if date_type:
                        new_date.attrib['type'] = date_type
                    if date_analog:
                        new_date.attrib['encodinganalog'] = date_analog
                    new_date.text = raw_input("Enter the text for date " + str(index) + ": ")
                    date_parent.insert(origin_index + index, new_date)
                    changed_dates += 1
                    index += 1
                date_parent.remove(date)
        outfile = open(join(path, filename), 'w')
        outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
        outfile.close()
