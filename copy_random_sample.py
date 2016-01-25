import shutil
import os
from os.path import join
import random

source_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
dest_path = 'C:/Users/djpillen/GitHub/test_run/ead'

source_eads = os.listdir(source_path)

copied = 0

while copied < 100:
	source_ead = random.choice(source_eads)
	source_eads.remove(source_ead)
	source_ead_path = join(source_path, source_ead)
	dest_ead_path = join(dest_path, source_ead)
	print "Copying {0} / 50: {1}".format(copied+1, source_ead)
	shutil.copy(source_ead_path, dest_ead_path)
	copied += 1