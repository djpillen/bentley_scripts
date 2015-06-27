from lxml import etree
import re

ead = '<ead><physdesc><extent>2 lin ft 2 oversize v 4 oversize f</extent></physdesc></ead>'

tree = etree.XML(ead)

extents = tree.xpath('//extent')

correct = re.compile(r'^\d+\s((linear feet)|(oversize volumes))$')

for e in extents:
    if correct.match(e.text):
        continue
    else:
        initial_physdesc = e.getparent()
        initial_physdesc_parent = initial_physdesc.getparent()
        initial_extent_parent = initial_physdesc.getparent()
        initial_extent_index = initial_extent_parent.index(initial_physdesc)
        changed_extents = 0
        index = 1
        print e.text
        new_extents = int(raw_input("How many extents?: "))
        while changed_extents < new_extents:
            new_physdesc = etree.Element('physdesc')
            new_extent = etree.SubElement(new_physdesc, 'extent')
            new_extent.text = raw_input("Enter the text for extent " + str(index) + ": ")
            initial_extent_parent.insert(initial_extent_index + index, new_physdesc)
            changed_extents += 1
            index += 1
            initial_extent_parent.remove(initial_physdesc)

print etree.tostring(tree)
