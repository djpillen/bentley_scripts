import os
from os.path import join

from lxml import etree


def prettify_xml_in_directory(input_dir, output_dir):
    parser = etree.XMLParser(remove_blank_text=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            xml = etree.parse(join(input_dir, filename), parser)
            with open(join(output_dir, filename), mode='w') as f:
                f.write(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))


if __name__ == "__main__":
    input_directory = r'C:\Users\wboyle\PycharmProjects\vandura\Real_Masters_all'
    output_directory = r'c:\Users\wboyle\PycharmProjects\bentley_code\main_projects\authority_reconciliation\output_cleaned'
    prettify_xml_in_directory(input_directory, output_directory)