from lxml import etree
import os
from os.path import join
import csv


'''
# check for something like...
<physdesc>
<extent>2 tapes</extent>
</physdesc>
<physdesc>
<physfacet>VHS</physfacet>
</physdesc>
'''

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

save_file = 'C:/Users/Public/Documents/multiple_physdescs.csv'

count = 0
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		physdescs = component.xpath('./did/physdesc')
		if len(physdescs) > 1:
			extent = False
			no_extent = False
			for physdesc in physdescs:
				if not physdesc.xpath('./extent'):
					no_extent = True
				else:
					extent = True
			if no_extent and extent:
				'''
				first = physdescs[0]
				second = physdescs[1]
				for elem in second.xpath('./*'):
					first.append(elem)
				second.getparent().remove(second)
				'''
				with open(save_file,'ab') as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow([filename,tree.getpath(component)])
				print filename, tree.getpath(component)
				count += 1
	#with open(join(path,filename),'w') as ead_out:
		#ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	#print filename
print count

