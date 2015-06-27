from lxml import etree
import csv
from os.path import join

path = 'Real_Masters_all'

dates_file = 'dates_begin_after_end-to_check.csv'


backward_dates = {}

with open(dates_file, 'rb') as dates_csv:
    reader = csv.reader(dates_csv)
    next(reader, None)
    for row in reader:
        filename = row[0]
        date_path = row[1]
        if filename not in backward_dates:
            backward_dates[filename] = {}
        tree = etree.parse(join(path,filename))
        coll_title_path = tree.xpath('//archdesc/did/unittitle')
        coll_title = coll_title_path[0].text
        unitid = tree.xpath('//archdesc/did/unitid')
        unitid_text = unitid[0].text
        date = tree.xpath(date_path)
        date_text = date[0].text
        title_path = date[0].getparent()
        title = title_path[0].text
        did = title_path.getparent()
        container = did.xpath('./container')
        if container:
            container_type_num = container[0].attrib['type'] + ' ' + container[0].text
        else:
            container_type_num = 'Unknown'
        if 'Col_title' not in backward_dates[filename]:
            backward_dates[filename]['Col_title'] = coll_title
        if 'Unitid' not in backward_dates[filename]:
            backward_dates[filename]['Unitid'] = unitid_text
        if 'Backward' not in backward_dates[filename]:
            backward_dates[filename]['Backward'] = {}
        backward_dates[filename]['Backward'][date_path] = {}
        backward_dates[filename]['Backward'][date_path]['Unittitle'] = title
        backward_dates[filename]['Backward'][date_path]['Unitdate'] = date_text
        backward_dates[filename]['Backward'][date_path]['Container'] = container_type_num
        with open('backward_dates_info.csv','ab') as backward_file:
            writer = csv.writer(backward_file)
            writer.writerow([filename, coll_title, unitid_text, container_type_num, date_text, date_path])


print backward_dates['beeton.xml']

"""

document = Document()

for filename in access_restrictions:
    document.add_heading(access_restrictions[filename]['Title'])
    document.add_heading('Collection Level Restriction', level=2)
    document.add_paragraph(access_restrictions[filename]['Restriction'])
    document.add_heading('Expired Restrictions', level=2)
    table = document.add_table(rows=1, cols=3)
    table.autofit = True
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Container"
    hdr_cells[1].text = 'Expiration Date'
    hdr_cells[2].text = 'Full Restriction'
    for date_path in access_restrictions[filename]['Expired']:
        row_cells = table.add_row().cells
        row_cells[0].text = access_restrictions[filename]['Expired'][date_path]['Container_number']
        row_cells[1].text = access_restrictions[filename]['Expired'][date_path]['Expiration_date']
        row_cells[2].text = access_restrictions[filename]['Expired'][date_path]['Full_text']


    table.style= "TableGrid"
    document.add_paragraph('Remaining Time-Bound Restrictions')
    document.add_paragraph(access_restrictions[filename]['Remaining_time'])
    document.add_paragraph('Remaining Non-Time-Bound Restrictions')
    document.add_paragraph(access_restrictions[filename]['Remaining_non_time'])
    document.add_page_break()

document.save('test.docx')
"""
