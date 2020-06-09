import ASFunctions as asf
# from pymarc import MARCReader
# import requests
import os
import json
from pprint import pprint
from sheetFeeder import dataSheet
import dcps_utils as util


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    # sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'
    sheet_id = '1e43qKYvqGQFOMxA70U59yPKPs18y-k3ohRNdU-qrTH0'  # test

    container_sheet = dataSheet(
        sheet_id, 'containers!A:Z')

    marc_sheet = dataSheet(
        sheet_id, 'marc!A:Z')

    # Get a list of bibids from the Marc tab.
    the_bibids = marc_sheet.getDataColumns()[0]
    the_bibids.pop(0)
    the_bibids = list(set(the_bibids))
    print(the_bibids)

    #### TOP CONTAINERS ####

    the_heads = ['bibid', 'resource', 'uri',
                 'type', 'display_string', 'concat']
    the_rows = [the_heads]

    lookup_csv = os.path.join(my_path, 'id_lookup_prod.csv')
    for abib in the_bibids:
        print(abib)
        # Get repo and asid from bibid
        repo, asid = asf.lookupByBibID(abib, lookup_csv)

        print('Getting top containers for ' + str(repo) + ':' + str(asid))

        the_query = '/repositories/' + \
            str(repo) + '/resources/' + str(asid) + '/top_containers'

        # list of top containers
        the_refs = json.loads(asf.getResponse(the_query))

        cnt = 0
        for r in the_refs:
            cnt += 1
            print(cnt)
            try:
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
                try:
                    concat_str = str(
                        tc['display_string'] + ' (' + uri.split('/')[4]) + ')'

                except:
                    concat_str = 'x'

                a_row = [bibid, resource, uri, type,
                         display_string, concat_str]
                # print(a_row)
                the_rows.append(a_row)
            except:
                print(r)

    # Write results to google sheet
    container_sheet.clear()
    z = container_sheet.appendData(the_rows)
    print(z)


if __name__ == "__main__":
    main()
