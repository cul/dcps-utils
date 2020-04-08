from pymarc import MARCReader
import requests
import os
from pprint import pprint
from sheetFeeder import dataSheet


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'

    container_sheet = dataSheet(
        sheet_id, 'containers!A:Z')

    marc_sheet = dataSheet(
        sheet_id, 'marc!A:Z')

    the_ids = [[2, 5337, 6911309]]

    for id in the_ids:
        repo = id[0]
        asid = id[1]
        bibid = id[2]

    # Get and save the MARC
    marc_path = os.path.join(my_path, 'output/' + str(bibid) + '.marc')

    x = get_clio_marc(bibid)

    with open(marc_path, 'wb') as f:
        f.write(x)

    # Read the MARC

    the_heads = ['bibid', 'display_string', '876$0', '876$a', '876$p']

    the_rows = [the_heads]

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

    # print(the_rows)
    marc_sheet.clear()

    x = marc_sheet.appendData(the_rows)
    print(x)


def get_clio_marc(bibid):
    url = 'https://clio.columbia.edu/catalog/' + str(bibid) + '.marc'
    response = requests.get(url)
    return response.content


if __name__ == "__main__":
    main()
