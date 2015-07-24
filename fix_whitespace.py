import os
import re

from prettifydirectory import prettify_xml_in_directory


def fix_whitespace(input_dir, output_dir):
	whitespace_regex = r"\s{2,}|\v"
	eads = [ead for ead in os.listdir(input_dir) if ead.endswith(".xml")]
	for ead in eads:
		with open(os.path.join(input_dir, ead), mode="r") as f:
			data = f.read()

		data = " ".join(re.split(whitespace_regex, data))

		with open(os.path.join(output_dir, ead), mode="w") as f:
			f.write(data)

	prettify_xml_in_directory(input_dir=output_dir, output_dir=output_dir)

fix_whitespace('C:/Users/Public/Documents/s_master-2', 'C:/Users/Public/Documents/s_master')
