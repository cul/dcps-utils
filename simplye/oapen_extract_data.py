# Script to harvest data from the OAPEN api (library.oapen.org/rest) for use in composing OPDS feed. The list of ids is obtained from a spreadsheet (cols 6 or 7 in this case). The ids are queried using dc.identifier parameter.
#
# Example query: https://library.oapen.org/rest/search?query=dc.identifier:627426&expand=metadata,bitstreams,parentCollection
#
# The script also merges an ILS BIBID (id[0]) into the output for later use in linking back to catalog.
# Result is a pickled dictionary. This is in turn read by another script (oapen_build_opds) to build OPDS XML file(s).


import dcps_utils as util
import requests
import json
from sheetFeeder import dataSheet
from pprint import pprint
from datetime import datetime


def main():

    # x = get_oapen_item(627426)
    # pprint(x)

    # quit()

    now = datetime.today().isoformat()  # Current timestamp in ISO

    the_sheet = dataSheet(
        '1kLI8x1whzSNqeKL5xVysopgKYWE9-D9H_PHX2RkW4wQ', 'ingest!A:Z')

    the_inputs = the_sheet.getData()
    the_inputs.pop(0)

    # divide the data into chunks of 500
    the_chunks = divide_list(the_inputs, 500)

    for idx, data_chunk in enumerate(the_chunks):

        page_no = idx + 1

        # name the output files in increments
        out_path = 'output/oapen_clio/oapen_extract_' + \
            str(page_no) + '.pickle'

        the_data = []

        for i in data_chunk:
            if len(i) >= 7:
                if not(i[0]):
                    print("No bibid for " + str(id) + "! Skipping...")
                    continue

                bibid = i[0]
                if i[6] or i[7]:
                    if i[6]:
                        id = i[6]
                    else:
                        id = i[7]
                    id_data = get_oapen_item(id)
                    # id_data = json.loads(requests.get(query).text)
                    # pprint(id_data)
                    if len(id_data) != 1:
                        # no entries returned, or more than one (!) returned.
                        print('Either no data or multiple matches for ' +
                              id + '. Skipping...')
                    else:
                        id_data[0]['cul_bibid'] = bibid

                        print('Saving data for ' + id + '...')
                        # pprint(id_data[0])

                        # for e in id_data[0]['metadata']:
                        #     if e['element'] == 'description':
                        #         e['value'] += '\nView in CLIO: https://clio.columbia.edu/catalog/' + bibid

                        the_data.append(id_data[0])

        # for x in the_data:
        #     print(x['link'])

        util.pickle_it(the_data, out_path)


def get_oapen_item(_id):
    base_url = 'https://library.oapen.org/rest/search'
    query = base_url + '?query=dc.identifier:' + \
        str(_id) + '&expand=metadata,bitstreams,parentCollection'
    # print(query)
    r = requests.get(query)
    r.encoding = 'UTF-8'
    id_data = json.loads(r.text)
    # pprint(id_data)
    return id_data


def divide_list(lst, n):
    # generate n-sized chunks from list.
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    main()
