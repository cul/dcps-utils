from lxml import etree

import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet
from operator import itemgetter
import datetime
import re
import os
import logging
import dcps_utils as util


logging.basicConfig(level=logging.ERROR)
# not doing anything with this yet...

# logging.debug('¥¥¥¥¥¥ This is a debug message')
# logging.info('¥¥¥¥¥¥ This is an info message')
# logging.warning('¥¥¥¥¥¥ This is a warning message')
# logging.error('¥¥¥¥¥¥ This is an error message')
# logging.critical('¥¥¥¥¥¥ This is a critical message')


my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

asf.setServer('Prod')

print('THIS IS A TEST -- IGNORE!')

print(' ')


print('testing google sheet api...')

# The ID and range of a sample spreadsheet.
the_sheet = dataSheet(
    '1YzM1dinagfoTUirAoA2hHBfnhSM1PsPt8TkwTT9KlgQ', 'Sheet1!A:Z')
# the_sheet = dataSheet('1YzM1oTUirAoA2hHBfnhSM1PsPt8TkwTT9KlgQ','Sheet1!A:Z')


print(the_sheet.getData())

print(' ')

x = the_sheet.matchingRows([['BIBID', '4079432'], ['Title', '.*Humph.*']])

print(x)

print(' ')

x = the_sheet.lookup('4079432', 0, 1)

print(x)

print(' ')

print('testing archivesspace api...')

x = asf.getResource(2, 5907)

print(x)

print(' ')

print("testing saxon ...")

# saxon_path = os.path.join(my_path, '/opt/dcps/resources/saxon-9.8.0.12-he.jar')
source_dir = '/cul/cul0/ldpd/archivesspace/oai'
in_file = os.path.join(source_dir, '20210101.asClean.xml')
xsl_file = os.path.join(my_path, '../xslt/extract-bibids.xsl')
params = 'filename=' + in_file
x = util.saxon_process2(in_file, xsl_file, None, theParams=params)
print(x)

print("This is a test!")

print("Yes it worked...")
