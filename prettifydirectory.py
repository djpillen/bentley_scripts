import re
import os
from os.path import join

from lxml import etree
from tqdm import tqdm


def prettify_xml_in_directory(input_dir, output_dir):
    parser = etree.XMLParser(remove_blank_text=True)
    for filename in tqdm(os.listdir(input_dir), desc="Prettify progress", leave=True):
        if filename.endswith(".xml"):
            # first, prettyprint with the custom parser
            xml = etree.parse(join(input_dir, filename), parser)
            with open(join(output_dir, filename), mode='w') as f:
                f.write(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))

            # now re-iterate with the whitespace fix
            xml = etree.parse(join(output_dir, filename))
            with open(join(output_dir, filename), mode="w") as f:
                fixed_text = fix_prettyprint_whitespace(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))
                f.write(fixed_text)


def fix_prettyprint_whitespace(raw_text):
    open_to_close_tag_regex = r'(\<\/.*?\>)(\<[^\/]*?\>)'
    item_regex = r'(\<\/item\>)\ (\<item\>)'

    text = re.sub(open_to_close_tag_regex, r'\g<1> \g<2>', raw_text)
    text = re.sub(item_regex, r'\g<1>\g<2>', text)

    return text

if __name__ == "__main__":
    input_directory = r'C:\Users\Public\Documents\normalized'
    output_directory = r'C:\Users\Public\Documents\s_master'
    prettify_xml_in_directory(input_directory, output_directory)
