from lxml import etree
import os
from os.path import join
import csv
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    unittitles = tree.xpath('//unittitle')
    for unittitle in unittitles:
        dates_normal = []
        dates_text = []
        unitdates = unittitle.xpath('.//unitdate')
        for unitdate in unitdates:
            if 'normal' in unitdate.attrib:
                if unitdate.attrib['normal'] not in dates_normal:
                    dates_normal.append(unitdate.attrib['normal'])
                elif unitdate.attrib['normal'] in dates_normal:
                    print 'Duplicate normalized dates in',filename,':',etree.tostring(unittitle)
                    with open('C:/Users/Public/Documents/repeated_dates.csv','ab') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([filename, tree.getpath(unittitle),etree.tostring(unittitle)])
                    '''
            if unitdate.text is not None:
                if unitdate.text not in dates_text:
                    dates_text.append(unitdate.text)
                elif unitdate.text in dates_text:
                    print 'Duplicate text in',filename,':',etree.tostring(unittitle)
                    '''
