import ia_build_opds as ia
from sheetFeeder import dataSheet
from pprint import pprint
import dcps_utils as util


the_sheet = dataSheet(
    '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'LingLong!A:Z')

output_folder = 'output/ia/ll/'

the_input = the_sheet.getData()
heads = the_input.pop(0)

the_data = []

for y in range(1931, 1938):
    the_data.append({'vol': y, 'items': [{'bibid': r[0], 'id': r[2]}
                                         for r in the_input if r[1] == str(y)]})

pprint(the_data)

for vol_data in the_data:
    print(' ')
    print(vol_data['vol'])
    feed_stem = 'ia_ll_' + str(vol_data['vol'])
    # print(vol_data['items'])
    the_extracts = ia.extract_data(
        vol_data['items'], feed_stem, 'Ling Long (' + str(vol_data['vol']) + ')')

    pprint(the_extracts['errors'])
    # pprint(the_extracts['data'][0]['description'])

    util.pickle_it(the_extracts['data'], output_folder + feed_stem + '.pickle')

quit()
