from lxml import etree

old_file = 'S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/Master_20150504-Original_EADs/nispodcast.xml'
new_file = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all/nispodcast.xml'
new_new_file = 'C:/Users/djpillen/GitHub/test_dir/nispodcast.xml'

def dao_abstract_check(ead):
    dao_abstract_count = 0
    tree = etree.parse(ead)
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for component in components:
        dao = component.xpath('./did/dao')
        abstract = component.xpath('./did/abstract')
        note = component.xpath('./did/note')
        if abstract and dao:
            print tree.getpath(component)
            dao_abstract_count += 1
    return dao_abstract_count

def dao_odd_check(ead):
    dao_odd_count = 0
    tree = etree.parse(ead)
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for component in components:
        daos = component.xpath('./did/dao')
        odds = component.xpath('./odd/p')
        if daos and odds:
            print tree.getpath(component)
            dao_odd_count += 1
    return dao_odd_count

def dao_odd_fix(ead):
    tree = etree.parse(ead)
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for component in components:
        daos = component.xpath('./did/dao')
        odds = component.xpath('./odd/p')
        if daos and odds:
            for odd in odds:
                abstract_text = odd.text
                abstract = etree.Element('abstract')
                abstract.text = abstract_text
                did = daos[0].getparent()
                did.append(abstract)
                odd_to_remove = odd.getparent()
                component.remove(odd_to_remove)
    new_new_file = open('C:/Users/djpillen/GitHub/test_dir/nispodcast.xml','w')
    new_new_file.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def odd_fix(ead):
    tree = etree.parse(ead)
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for component in components:
        odds = component.xpath('./odd/p')
        dids = component.xpath('./did')
        for odd in odds:
            odd_text = odd.text
            if not odd_text.startswith('('):
                abstract_text = odd_text
                abstract = etree.Element('abstract')
                abstract.text = abstract_text
                did = dids[0]
                did.append(abstract)
                odd_to_remove = odd.getparent()
                component.remove(odd_to_remove)
    new_new_file = open('C:/Users/djpillen/GitHub/test_dir/nispodcast.xml','w')
    new_new_file.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

#dao_abstract_count = dao_abstract_check(new_new_file)
#dao_odd_count = dao_odd_check(new_new_file)
#print dao_abstract_count
#print dao_odd_count

odd_fix(new_file)
