# Script to get top containers from a list and replace the indicators
# (e.g., I.1) with modified ones. See ACFA-280.

import ASFunctions as asf
import json
# from pprint import pprint
from sheetFeeder import dataSheet
# import dcps_utils as util
import os.path

SERVER = 'Prod'
asf.setServer(SERVER)

# pprint(json.loads((asf.getTopContainer(2, 69730))))
# quit()

my_name = __file__

# This makes sure the script can be run from any working directory
# and still find related files.
my_path = os.path.dirname(__file__)

sheet_id = '13OakaS0KHtxcaV9HGWDP9Zfnz9TVJR_9zGUnKrb90jk'

in_sheet = dataSheet(sheet_id, 'batch!A:Z')
# in_sheet = dataSheet(sheet_id, 'test!A:Z')  # test
out_sheet = dataSheet(sheet_id, 'output!A:Z')


the_data = in_sheet.getData()

the_heads = the_data.pop(0)

new_data = [['asid', 'ind_old', 'ind_new', 'verify']]  # heads

for a_row in the_data:
    asid = a_row[0]
    ind_new = a_row[1]
    x = json.loads(asf.getTopContainer(2, asid))
    ind_old = x['indicator']
    print(str(asid) + ' - ' + ind_old + ' | ' + ind_new)
    x['indicator'] = ind_new
    if ind_old != ind_new:
        resp = asf.postTopContainer(2, asid, json.dumps(x))
        print(resp)
        verify = json.loads(asf.getTopContainer(2, asid))['display_string']
    else:
        print("Identical: skipping!")
        verify = '(Skipped)'
    new_data.append([str(asid), ind_old, ind_new, verify])

out_sheet.clear()
out_sheet.appendData(new_data)

# print(new_data)
