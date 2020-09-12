import ASFunctions as asf
from pymarc import MARCReader
import os
import json
from pprint import pprint
from sheetFeeder import dataSheet
import dcps_utils as util
import csv


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    sheet_id = '1bTD8J33d1gbNlP-93XzJ7R0_wju2lPOdVmf8Hw7JSzU'
    # sheet_id = '1e43qKYvqGQFOMxA70U59yPKPs18y-k3ohRNdU-qrTH0'  # test

    # container_sheet = dataSheet(
    #     sheet_id, 'containers!A:Z')

    marc_sheet = dataSheet(
        sheet_id, 'marc!A:Z')

    holding_sheet = dataSheet(
        sheet_id, 'holdings!A:Z')

    the_bibids = []
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-single-holdings_TEST.csv' # test
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-batch_4.csv'
    aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-mult-holdings_1.csv'
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/biblist_test.csv'

    the_bibs = open(aCSV)
    for row in csv.reader(the_bibs):
        the_bibids.append(row[0])
    the_bibs.close()

    # print(the_bibids)

    ### MARC ###

    # Read the MARC

    the_heads = ['bibid', 'holding_id', '876$a', '876$p', 'display_string']
    the_rows = [the_heads]

    the_holdings = [['bibid', 'holding_id', 'holding_desc']]

    for abib in the_bibids:
        print('Getting MARC for ' + str(abib))

        marc_path = os.path.join(my_path, 'output/marc/' + str(abib) + '.marc')

        with open(marc_path, 'rb') as fh:
            reader = MARCReader(fh)
            for record in reader:

                the_852s = record.get_fields('852')
                the_099 = record.get_fields('099')
                the_bibid = the_099[0].get_subfields('a')[0]
                the_876s = record.get_fields('876')

                # Get holding record info
                for r in the_852s:
                    the_852_data = [
                        str(abib),
                        r.get_subfields(
                            '0')[0],
                        r.get_subfields('h')[0]
                    ]
                    the_holdings.append(the_852_data)

                print(len(the_876s))

                cnt = 1
                for r in the_876s:
                    cnt += 1
                    # Need to specify order of subfields explicitly
                    the_876_data = [
                        r.get_subfields('0'),
                        r.get_subfields('a'),
                        r.get_subfields('p'),
                        r.get_subfields('3')
                    ]
                    the_row = []
                    for d in the_876_data:
                        try:
                            dd = d[0]
                        except:
                            dd = ""
                        the_row.append(dd)

                    # the_row = [
                    #     r.get_subfields('3')[0],
                    #     r.get_subfields('0')[0],
                    #     r.get_subfields('a')[0],
                    #     r.get_subfields('p')[0]
                    # ]

                    # print(the_row)

                    the_row.insert(0, str(abib))
                    # the_row.insert(
                    #     5, '=VLOOKUP($B' + str(cnt) + ',holdings!B:C,2,false)')

                    the_rows.append(the_row)

    # Write results to google sheet

    marc_sheet.clear()
    x = marc_sheet.appendData(the_rows)
    print(x)

    holding_sheet.clear()
    x = holding_sheet.appendData(the_holdings)
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
