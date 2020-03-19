import os
from lxml import etree as et
import ASFunctions as asf
import datetime

today = datetime.datetime.today().strftime("%Y%m%d")

# Test
today = '20190721'


xml_folder = '/cul/cul0/ldpd/archivesspace/updates'
output_folder = '/opt/dcps/archivesspace/output/ead'

id_xml = xml_folder + '/' + today + '.asDeltaIds.xml'

# ns = {"marc": "http://www.loc.gov/MARC21/slim"}

tree = et.parse(id_xml)
root = tree.getroot()


the_recs = root.findall('record')

the_ids = []

for a_rec in the_recs:
    i = a_rec.xpath('identifier/text()')

    asid = str(i[0].split('/')[-1]).rstrip() # get the asid from the uri string.
    repo = str(i[0].split('/')[-3]).rstrip() # get the repo from the uri string.
    bibid = a_rec.xpath('bibid/text()')[0]

    the_ids.append([repo,asid,bibid])


for x in the_ids:

    the_ead = asf.getEAD(x[0],x[1])

    out_path = output_folder + '/' + str(x[2]) + '_out.xml'

    # Save copy of existing object
    print('Saving data to ' + out_path + '....')

    f = open(out_path, "w+")
    f.write(the_ead)
    f.close()



