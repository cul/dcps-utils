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

    # sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'
    # sheet_id = '1e43qKYvqGQFOMxA70U59yPKPs18y-k3ohRNdU-qrTH0'  # test
    sheet_id = '1OhgJ4g-SWbmnms4b3ppe_0rBT7hz9jfQp6P8mADcatk'  # template doc

    container_sheet = dataSheet(
        sheet_id, 'containers!A:Z')

    marc_sheet = dataSheet(
        sheet_id, 'marc!A:Z')

    the_bibids = []
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-single-holdings_TEST.csv' # test
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-batch_8.csv'
    aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-batch_7.csv'
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-missing-batch-2.csv'
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-mult-holdings_1.csv'
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/biblist_test.csv'

    the_bibs = open(aCSV)
    for row in csv.reader(the_bibs):
        the_bibids.append(row[0])
    the_bibs.close()

    # print(the_bibids)

    ### MARC ###

    # Read the MARC

    the_heads = ['CONCAT', 'bibid',
                 'display_string', '876$0', '876$a', '876$p']
    the_rows = [the_heads]

    row_cnt = 2

    for abib in the_bibids:
        print('Getting MARC for ' + str(abib))

        marc_path = os.path.join(my_path, 'output/marc/' + str(abib) + '.marc')

        if os.path.exists(marc_path):

            with open(marc_path, 'rb') as fh:
                reader = MARCReader(fh)
                for record in reader:
                    # Find out if there is more than one holding; if there is, we cannot use it to automatically match top containers by name and will skip.
                    the_852s = record.get_fields('852')
                    if len(the_852s) > 1:
                        print("More than one holding record (" +
                              str(len(the_852s)) + "). Skipping.")
                    else:
                        the_099 = record.get_fields('099')
                        the_bibid = the_099[0].get_subfields('a')[0]
                        the_876s = record.get_fields('876')

                        print(len(the_876s))
                        for r in the_876s:
                            # Need to specify order of subfields explicitly
                            the_876_data = [
                                r.get_subfields('3'),
                                r.get_subfields('0'),
                                r.get_subfields('a'),
                                r.get_subfields('p')
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

                            # concat_str = '=B' + \
                            #     str(row_cnt) + ' & ": " & C' + str(row_cnt)
                            concat_str = str(abib) + ": " + str(the_row[1])
                            the_row.insert(0, concat_str)

                            the_rows.append(the_row)
                            row_cnt += 1  # increment row num used in CONCAT
        else:
            print("Could not find " + marc_path + "... skipping...")

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
