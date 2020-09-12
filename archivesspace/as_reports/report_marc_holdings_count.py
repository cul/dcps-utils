# Script to report counts of 852s in MARC records.

from pymarc import MARCReader
import os
import json
from pprint import pprint
from sheetFeeder import dataSheet
import dcps_utils as util
# import csv


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'

    bibids_sheet = dataSheet(
        sheet_id, 'MARC-exported!A:Z')
    holding_counts_sheet = dataSheet(
        sheet_id, 'holding_counts!A:Z')

    the_bibids = [r[0] for r in bibids_sheet.getData()]

    ### MARC ###

    # Read the MARC

    the_heads = ['bibid', 'holdings_count']
    the_rows = [the_heads]

    for abib in the_bibids:
        print('Getting MARC for ' + str(abib))

        marc_path = os.path.join(my_path, 'output/marc/' + str(abib) + '.marc')

        if os.path.exists(marc_path):

            try:
                with open(marc_path, 'rb') as fh:
                    reader = MARCReader(fh)
                    for record in reader:
                        # Find out if there is more than one holding; if there is, we cannot use it to automatically match top containers by name and will skip.
                        the_852s = record.get_fields('852')
                        count_852s = len(the_852s)

            except Exception as error:
                count_852s = 'ERROR: ' + str(error)
            the_rows.append([abib, str(count_852s)])

        else:
            print("Could not find " + marc_path + "... skipping...")

    # print(the_rows)
    holding_counts_sheet.clear()
    x = holding_counts_sheet.appendData(the_rows)
    print(x)

    quit()
    # Write results to google sheet

    marc_sheet.clear()
    x = marc_sheet.appendData(the_rows)
    print(x)

    quit()

    # ###
    # #### TOP CONTAINERS ####
    # container_sheet.clear()

    # the_heads = ['bibid', 'resource', 'uri', 'type', 'display_string']
    # the_rows = [the_heads]

    # for id in the_ids:
    #     repo = id[0]
    #     asid = id[1]

    #     print('Getting top containers for ' + str(repo) + ':' + str(asid))

    #     the_query = '/repositories/' + \
    #         str(repo) + '/resources/' + str(asid) + '/top_containers'

    #     # list of top containers
    #     the_refs = json.loads(asf.getResponse(the_query))

    #     cnt = 0
    #     for r in the_refs:
    #         cnt += 1
    #         print(cnt)
    #         try:
    #             tc = json.loads(asf.getResponse(r['ref']))
    #             # print(tc)

    #             try:
    #                 bibid = tc['collection'][0]['identifier']
    #             except:
    #                 bibid = ''
    #             try:
    #                 resource = tc['collection'][0]['ref']
    #             except:
    #                 resource = ''
    #             try:
    #                 uri = tc['uri']
    #             except:
    #                 uri = ''
    #             try:
    #                 type = tc['type']
    #             except:
    #                 type = ''
    #             try:
    #                 display_string = tc['display_string']
    #             except:
    #                 display_string = ''

    #             a_row = [bibid, resource, uri, type, display_string]
    #             # print(a_row)
    #             the_rows.append(a_row)
    #         except:
    #             print(r)

    # # Write results to google sheet
    # container_sheet.clear()
    # z = container_sheet.appendData(the_rows)
    # print(z)


def get_clio_marc(bibid):
    url = 'https://clio.columbia.edu/catalog/' + str(bibid) + '.marc'
    response = requests.get(url)
    return response.content


if __name__ == "__main__":
    main()
