from lxml import etree
import urllib2
import urlparse
from os.path import join
import os
import time

dspace_mets_dir = 'C:/Users/djpillen/GitHub/dspace_mets'
dspace_ids_file = 'C:/Users/djpillen/Downloads/dspace_ids.txt'
with open(dspace_ids_file) as f:
	dspace_ids_plain = f.read()
	dspace_ids_list = set(dspace_ids_plain.splitlines())

print "Found {0} dspace_ids".format(len(dspace_ids_list))

ids_to_fetch = [dspace_id for dspace_id in dspace_ids_list if dspace_id+".xml" not in os.listdir(dspace_mets_dir)]
print "Found {0} unfetched dspace_ids".format(len(ids_to_fetch))
count = 1
for dspace_id in ids_to_fetch:
	if dspace_id + '.xml' not in os.listdir(dspace_mets_dir):
		mets = "http://deepblue.lib.umich.edu/metadata/handle/2027.42/" + dspace_id + "/mets.xml"
		print "{0} - Fetching {1}".format(count, mets)
		page = urllib2.urlopen(mets)
		metstree = etree.parse(page)
		with open(join(dspace_mets_dir, dspace_id + '.xml'),'w') as mets_out:
			mets_out.write(etree.tostring(metstree))
		time.sleep(15)
	else:
		print "{0} - {1} already fetched".format(count, dspace_id)
	count += 1

series_extents = {}

for dspace_id in dspace_ids_list:
	print "Parsing sizes from {0}".format(dspace_id)
	metstree = etree.parse(join(dspace_mets_dir, dspace_id + '.xml'))
	ns = {'mets':'http://www.loc.gov/METS/','dim': 'http://www.dspace.org/xmlns/dspace/dim','xlink':'http://www.w3.org/TR/xlink/'}
	XLINK = 'http://www.w3.org/TR/xlink/'
	title = metstree.xpath("//dim:field[@element='title']", namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'})[0].text.strip().encode('utf-8')
	series = title.split('-')[0].strip()
	fileGrp = metstree.xpath("//mets:fileGrp[@USE='CONTENT']",namespaces=ns)[0]
	bitstreams = fileGrp.xpath('./mets:file',namespaces=ns)
	for bitstream in bitstreams:
		component_size = int(bitstream.attrib['SIZE'])
		series_extents[series] = series_extents.get(series, 0) + component_size

for series in series_extents:
	print "{0} - {1} bytes".format(series, series_extents[series])