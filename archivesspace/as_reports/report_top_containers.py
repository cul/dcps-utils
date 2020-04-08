from pymarc import MARCReader
import requests
import os
import json
from pprint import pprint
from sheetFeeder import dataSheet


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

    # The collections to process (repo, asid, bibid)
    the_ids = [[2, 5337, 6911309]]

    container_sheet.clear()

    ### MARC ###

    # Get and save the MARC

    # Read the MARC

    the_heads = ['bibid', 'display_string', '876$0', '876$a', '876$p']
    the_rows = [the_heads]

    for id in the_ids:
        bibid = id[2]
        print('Getting MARC for ' + str(bibid))

        x = get_clio_marc(bibid)

        marc_path = os.path.join(my_path, 'output/' + str(bibid) + '.marc')

        with open(marc_path, 'wb') as f:
            f.write(x)

        with open(marc_path, 'rb') as fh:
            reader = MARCReader(fh)
            for record in reader:
                the_099 = record.get_fields('099')
                the_bibid = the_099[0].get_subfields('a')[0]
                the_876s = record.get_fields('876')

                for r in the_876s:
                    # Need to specify order of subfields explicitly
                    the_row = [
                        r.get_subfields('3')[0],
                        r.get_subfields('0')[0],
                        r.get_subfields('a')[0],
                        r.get_subfields('p')[0]
                    ]

                    # print(the_row)

                    the_row.insert(0, the_bibid)

                    the_rows.append(the_row)

        # Write results to google sheet
        marc_sheet.clear()
        x = marc_sheet.appendData(the_rows)
        print(x)

    ###
    #### TOP CONTAINERS ####

    the_heads = ['bibid', 'resource', 'uri', 'type', 'display_string']
    the_rows = [the_heads]

    for id in the_ids:
        repo = id[0]
        asid = id[1]

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

                a_row = [bibid, resource, uri, type, display_string]
                # print(a_row)
                the_rows.append(a_row)
            except:
                print(r)

    # Write results to google sheet
    container_sheet.clear()
    z = container_sheet.appendData(the_rows)
    print(z)


def get_clio_marc(bibid):
    url = 'https://clio.columbia.edu/catalog/' + str(bibid) + '.marc'
    response = requests.get(url)
    return response.content


if __name__ == "__main__":
    main()
