from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    changed = False
    for component in components:
        containers = component.xpath('./did/container')
        if len(containers) > 1:
            if 'othertype' in containers[1].attrib['type']:
                label = containers[1].attrib['label']
                indicator = containers[1].text
                containers[1].text = label + ' ' + indicator
                changed = True
    if changed:
        print filename
        with open(join(path,filename),'w') as ead_out:
            ead_out.write(etree.tostring(tree,encoding="utf-8", xml_declaration=True))
