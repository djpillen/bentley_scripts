import lxml
from lxml import etree
import os
from os.path import join

path = 'Real_Masters_all'


testsubjects = []
subjects = {}
links = {}
abstracts = {}
coltitles = {}

for filename in os.listdir(path):
    print filename
    subjects[filename] = []
    links[filename] = []
    abstracts[filename] = []
    coltitles[filename] = []
    tree = etree.parse(join(path, filename))
    controlaccess = tree.xpath('//controlaccess/*')
    abstract = tree.xpath('//abstract')
    eadid = tree.xpath('//eadid')
    coltitle = tree.xpath('//archdesc/did/unittitle')
    for sub in controlaccess:
        if sub.tag == 'subject' or sub.tag == 'corpname' or sub.tag == 'geogname' or sub.tag == 'persname' or sub.tag == 'genreform' or sub.tag == 'famname':
            if sub.text is not None and sub.text not in subjects[filename]:
                subjects[filename].append(sub.text)
                testsubjects.append(sub.text)
    for number in eadid:
        links[filename].append('http://quod.lib.umich.edu/b/bhlead/'+number.text)
    for stuff in abstract:
        abstracts[filename].append(stuff.text)
    for title in coltitle:
        coltitles[filename].append(title.text)

print '\n\n\n'

whatsubj = raw_input("Pick a subject: ")
itsokay = 0
while itsokay < 1:
    if whatsubj in testsubjects:
        print 'Okay!'
        itsokay += 1
    else:
        whatsubj = raw_input("Try again: ")

       
subjectguide_web = whatsubj + '.html'
fout = open(subjectguide_web, 'a')
fout.write ('<body>')
fout.close()

print '\n\n\n\n'
for k in subjects:
    if whatsubj in subjects[k]:
        print 'File: ' + k
        print 'Collection title: ', " ".join(coltitles[k])
        title = " ".join(coltitles[k])
        print 'Link: ', " ".join(links[k])
        link = " ".join(links[k])
        print 'Abstract: ', " ".join(abstracts[k])
        abstract = " ".join(abstracts[k])
        fout = open(subjectguide_web, 'a')
        fout.write('<div><p><a href="'+link+'">'+title+'</a></p><p>'+abstract+'</p></div>')
        fout.close()

fout = open(subjectguide_web, 'a')
fout.write('</body>')
fout.close()
