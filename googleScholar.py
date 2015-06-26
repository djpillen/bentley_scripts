# import what we need
import urllib2
from bs4 import SoupStrainer, BeautifulSoup
import hashlib
import random
import lxml
from lxml import etree
import re
import string
import csv

# preliminary stuff
allcollections = []

# preliminary stuff for bhl
respdeepbluebhl = urllib2.urlopen('http://deepblue.lib.umich.edu/handle/2027.42/65133')
soupdeepbluebhl = BeautifulSoup(respdeepbluebhl.read())
artifactsbhl = soupdeepbluebhl.findAll("div", {"class": "artifact-title"})
for ibhl in artifactsbhl:
    abhl = ibhl.findAll('a')
    for iterbhl in abhl:
        hrefbhl = iterbhl.get('href')
        bhlcollection = hrefbhl.replace('/handle/2027.42/','')
        allcollections.append(bhlcollection)

# preliminary stuff for faculty archives
respdeepbluefa = urllib2.urlopen('http://deepblue.lib.umich.edu/handle/2027.42/79040')
soupdeepbluefa = BeautifulSoup(respdeepbluefa.read())
artifactsfa = soupdeepbluebhl.findAll("div", {"class": "artifact-title"})
for ifa in artifactsfa:
    afa = ifa.findAll('a')
    for iterfa in afa:
        hreffa = iterfa.get('href')
        facollection = hreffa.replace('/handle/2027.42/','')
        allcollections.append(facollection)

def checkgooglescholar(thecollectionid):
        
    # hack into google
    google_id = hashlib.md5(str(random.random())).hexdigest()[:16]
    google_headers = {'User-Agent' : 'Mozilla/5.0',
            'Cookie' : 'GSP=ID=%s:CF=4' % google_id }

    # deepblue stuff        
    deepbluebaseurl = 'http://deepblue.lib.umich.edu/handle/'
    deepbluecollectionid = str(thecollectionid)
    viewallitems = deepbluebaseurl + '2027.42/' + deepbluecollectionid + '/browse?'

    # google scholar stuff
    googlescholarbaseurl = 'https://scholar.google.com/scholar?hl=en&q='

    # function starts here

    # open and parse the deepblue html, find the artifacts we're after
    respdeepblue = urllib2.urlopen(viewallitems)
    soupdeepblue = BeautifulSoup(respdeepblue.read())
    artifacttitle = soupdeepblue.findAll("div", {"class": "artifact-title"})

    # loop to find bhl stuff cited in google scholar by handle
    for i in artifacttitle:
        a = i.findAll('a')
        # get handle
        for iter in a:
            href = iter.get('href')
            handle = href.replace('/handle/','')
            
            # deepblue item url
            deepblueitemurl = deepbluebaseurl + handle
            
            # google scholar item result
            googlescholarresult = googlescholarbaseurl + handle
            
            # do google search
            google_search = googlescholarbaseurl + handle
            request = urllib2.Request(google_search, headers=google_headers)
            response = urllib2.urlopen(request)
            html = response.read()
            
            # get to title <-- this can probably be cleaned up
            divwewant = html.find('<div class="gs_ri">')
            enddivwewant = html.find('</div>',divwewant)
            whatwewant = html[divwewant+1:enddivwewant]
            getpasthref = whatwewant.find('<a href=')
            endgetpasthref = whatwewant.find('>',getpasthref)
            endhref = whatwewant.find('</a>',endgetpasthref)
            title = whatwewant[endgetpasthref+1:endhref]
            
            # checkup
            print 'Processing Google Scholar... ' + title
            
            # get to description
            # getrest = html.find('div class="gs_a"')
            # endgetrest = html.find('</div>',getrest)
            # rest = html[getrest+17:endgetrest]
            
            # check to see if this is unique (i.e., not just a copy of something that's in deepblue)
            mets = "http://deepblue.lib.umich.edu/metadata/handle/" + handle + '/mets.xml'
            page = urllib2.urlopen(mets)
            metstree = etree.parse(page)
            deepbluetitlepath = metstree.xpath("//dim:field[@element='title']",namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'})
            deepbluetitle = deepbluetitlepath[0].text
            
            # create a temporary titles that will match <-- this could probably be improved
            fakedeepbluetitle = deepbluetitle.replace(' ', '')
            faketitle = title.replace(' ', '')
            for c in string.punctuation:
                fakedeepbluetitle = fakedeepbluetitle.replace(c, '')
                faketitle = faketitle.replace(c, '')
            if fakedeepbluetitle != faketitle:
                with open('C:/Users/Public/Documents/googlescholar.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([deepbluetitle, deepblueitemurl, title, googlescholarresult])

for itervar in allcollections:
    checkgooglescholar(itervar)