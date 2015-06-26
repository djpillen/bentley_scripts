import lxml.html
import re

links = lxml.html.parse("http://quod.lib.umich.edu/b/bhlead/umich-bhl-02160?view=text").xpath("//a/@href")
for link in links:
    daos = re.compile('awm00231')
    if daos.search(link):
        print link