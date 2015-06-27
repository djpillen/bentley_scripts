from lxml import etree
import os
from os.path import join
import re
import csv

def getdates():
    print "1) Output all unitdates to a csv"
    print "2) Output all unitdates to a csv that do not have a normal attribute or are not 'undated'"
    choice = raw_input("Enter a number: ")
    path = 'Real_Masters_all'
    if choice == "1":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            d = tree.xpath('//unitdate')
            for i in d:
                with open(outfile + '.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(i), i.text])
            print filename
        print outfile + '.csv complete'
    elif choice == "2":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            d = tree.xpath('//unitdate')
            for i in d:
                # yyyy = re.compile('^[\d]{4}s?$')
                # yyyy_yyyy = re.compile('^[\d]{4}s?[-][\d]{4}s?$')
                undated = re.compile('^[Uu]ndated$')
                if not undated.match(i.text) and not 'normal' in i.attrib:
                    with open(outfile + '.csv', 'ab') as csvfile:
                        writer = csv.writer(csvfile, dialect='excel')
                        writer.writerow([filename, tree.getpath(i), i.text])
            print filename
        print outfile + '.csv complete'

def getextents():
    print "1) Output only collection level extents to a csv"
    print "2) Output only component level extents to a csv"
    choice = raw_input("Enter a number: ")
    path = 'Real_Masters_all'
    if choice == "1":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            e = tree.xpath('//ead/archdesc/did//physdesc/extent')
            for e in e:
                extent = e.text or "EMPTY EXTENT"
                extentpath = tree.getpath(e)
                with open(outfile + '.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, extentpath, extent])
                csvfile.close()
            print filename
        print outfile + '.csv complete'
    elif choice == "2":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            e = tree.xpath('//dsc//did//extent')
            for e in e:
                extent = e.text or "EMPTY EXTENT"
                extentpath = tree.getpath(e)
                with open(outfile + '.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, extentpath, extent])
                csvfile.close()
            print filename
        print outfile + '.csv complete'

def getaccessrestrict():
    print '1) Output all accessrestrict statements to a csv'
    print '2) Output only collection level accessrestrict to a csv'
    print '3) Output only component level accessrestrict to a csv'
    print '4) Output only accessrestrict dates to a csv'
    choice = raw_input("Enter a number: ")
    path = 'Real_Masters_all'
    if choice == "1":
        outfile = raw_input("Enter a filename for the csv: ")
        print 'Note: The csv containing collection level accessrestrict statements will have a filename ending in toplevel and the csv containing component level accessrestrict statements will have a filename ending in componentlevel'
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            accesstop = tree.xpath('//archdesc/descgrp/accessrestrict')
            accesscomponent = tree.xpath('//archdesc/dsc//accessrestrict')
            for a in accesstop:
                with open(outfile + 'toplevel.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
            for a in accesscomponent:
                with open(outfile + 'componentlevel.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
            print filename
        print outfile + 'toplevel.csv and ' + outfile + ' componentlevel.csv complete'
    elif choice == "2":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            accesstop = tree.xpath('//archdesc/descgrp/accessrestrict')
            for a in accesstop:
                with open(outfile + '-collectionlevel.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
            print filename
        print outfile + '.csv complete'
    elif choice == "3":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            accesstop = tree.xpath('//archdesc/descgrp/accessrestrict')
            for a in accesscomponent:
                with open(outfile + 'componentlevel.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(a), etree.tostring(a)])
            print filename
        print outfile + '.csv complete'
    elif choice == "4":
        outfile = raw_input("Enter a filename for the csv: ")
        for filename in os.listdir(path):
            tree = etree.parse(join(path, filename))
            accessdate = tree.xpath('//archdesc/dsc//accessrestrict//date')
            for a in accessdate:
                if 'normal' in a.attrib:
                    normal = a.attrib['normal']
                else:
                    normal = ''
                with open(outfile + '.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, tree.getpath(a), a.text, normal, etree.tostring(a)])
            print filename
        print outfile + '.csv complete'

def getsubjects():
    pass

def start():
    print '1) Output content from <unitdate> tags to a csv'
    print '2) Output content from <extent> tags to a csv'
    print '3) Output content from <accessrestrict> tags to a csv'
    print '4) Output content from <subject>, <geogname>, <persname>, <genreform>, etc tags from <controlaccess> to a csv'

    choice = raw_input("Enter a number: ")

    if choice == "1":
        getdates()
    elif choice == "2":
        getextents()
    elif choice == "3":
        getaccessrestrict()
    elif choice == "4":
        getsubjects()
    else:
        print "Please enter one of the above numbers"

start()
