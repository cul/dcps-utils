# Script to add authorities or make other changes to subjects. See ACFA-287.

import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet
import os.path


SERVER = 'Prod'
asf.setServer(SERVER)

my_name = __file__


# pprint(asf.getSubject(11453))
# quit()

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

sheet_id = '1b-dFdOaWD7AEqzhK0uuGXkonum6wX8Zcriq8-G4l33Q'

# list_sheet = dataSheet(sheet_id, 'Test!A:Z')  # test
list_sheet = dataSheet(sheet_id, 'batch!A:Z')
report_sheet = dataSheet(sheet_id, 'output!A:Z')


def add_authority(server, asid, uri, source=None):
    # function to (1) query subject and determine if it already has
    # an authority uri, (2) if not, add in the provided URI,
    # and (3) return a response for reporting.
    subj = asf.getSubject(asid)
    if 'authority_id' in subj:
        print('*** Subject ' + str(asid) + ' already has authority: ' +
              subj['authority_id'] + ' .... Skiping....')
        return [server, asid, subj['authority_id'], subj['source'], 'Y']
    else:
        subj['authority_id'] = uri
        if source is None:
            source = subj['source']
            # If a new source is provided, add it in as well.
        else:
            subj['source'] = source
        try:
            resp = asf.postSubject(asid, json.dumps(subj))
        except json.JSONDecodeError as e:
            resp = 'JSON ERROR: + str(asid) + :: ' + str(e)
        except Exception as e:
            resp = 'ERROR: + str(asid) + :: ' + str(e)
        print(resp)
        return [server, asid, uri, str(source), '', str(resp)]


the_data = list_sheet.getData()

the_heads = the_data.pop(0)

full_output = [['server', 'asid', 'uri',
                'source', 'existing?', 'response']]  # heads

for a_row in the_data:
    asid = a_row[0].split('/')[2]
    uri = a_row[1]
    source = a_row[3] if len(a_row) >= 4 else None
    # print(str(asid))
    the_output = add_authority(SERVER, asid, uri, source=source)

    print(','.join(the_output))
    full_output.append(the_output)

report_sheet.clear()
report_sheet.appendData(full_output)
