import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet

asf.setServer('Test')


sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'

the_sheet = dataSheet(sheet_id, 'test!A:Z')


repo = 2
asid = 5102

the_query = '/repositories/' + \
    str(repo) + '/resources/' + str(asid) + '/top_containers'

# list of top containers
the_refs = json.loads(asf.getResponse(the_query))

the_rows = []


for r in the_refs:
    tc = json.loads(asf.getResponse(r['ref']))
    # print(tc)

    try:
        bibid = tc['collection'][0]['identifier']
    except:
        bibid = ''
    try:
        uri = tc['uri']
    except:
        uri = ''
    try:
        type = tc['type']
    except:
        type = ''
    try:
        display_string = tc['display_string']
    except:
        display_string = ''

    a_row = [bibid, uri, type, display_string]
    # print(a_row)
    the_rows.append(a_row)


the_sheet.clear()

z = the_sheet.appendData(the_rows)
print(z)
quit()

pprint(json.loads(x))

y = asf.getResponse('repositories/2/top_containers/89920')

print(' ')

pprint(json.loads(y))
