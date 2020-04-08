import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet

import requests


# def get_clio(bibid):
#     url = 'https://clio.columbia.edu/catalog/' + str(bibid) + '.marc'
#     response = requests.get(url)
#     return response.content


# print(get_clio('4079656'))

# quit()


asf.setServer('Prod')


sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'

the_sheet = dataSheet(sheet_id, 'containers!A:Z')

the_heads = ['bibid', 'resource', 'uri', 'type', 'display_string']
the_rows = [the_heads]

the_records = [[2, 5787], [2, 5337]]

for record in the_records:
    repo = record[0]
    asid = record[1]

    the_query = '/repositories/' + \
        str(repo) + '/resources/' + str(asid) + '/top_containers'

    # list of top containers
    the_refs = json.loads(asf.getResponse(the_query))

    for r in the_refs:
        tc = json.loads(asf.getResponse(r['ref']))
        # print(tc)

        try:
            bibid = tc['collection'][0]['identifier']
        except:
            bibid = ''
        try:
            resource = tc['collection'][0]['ref']
        except:
            resource = ''
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

        a_row = [bibid, resource, uri, type, display_string]
        # print(a_row)
        the_rows.append(a_row)


the_sheet.clear()

z = the_sheet.appendData(the_rows)
print(z)
