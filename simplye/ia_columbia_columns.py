import ia_opds_functions as ia
from sheetFeeder import dataSheet
from pprint import pprint
import dcps_utils as util


sheet_id = '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I'
sheet_tab = 'ColumbiaColumns'
the_in_sheet = dataSheet(sheet_id, sheet_tab + '!A:Z')
the_out_sheet = dataSheet(sheet_id, 'extract-errors!A:Z')

output_folder = 'output/ia/'
feed_stem = 'ia_cuc_feed'
collection_title = 'Columbia University Columns'
abbr = 'cuc'

pickle_path = output_folder + feed_stem + '.pickle'


the_input = the_in_sheet.getData()
heads = the_input.pop(0)

the_records = [{'bibid': r[0], 'id':r[2], 'label': r[3]} for r in the_input]

feed_data = ia.extract_data(the_records, feed_stem, collection_title)

print('Saving ' + str(len(feed_data['data'])
                      ) + ' records to ' + pickle_path)
util.pickle_it(feed_data['data'], pickle_path)

# pprint(feed_data['data'])
# pprint(feed_data['errors'])

the_out_sheet.appendData(feed_data['errors'])

# Generate the XML

the_err_sheet = dataSheet(
    sheet_id, 'errors!A:Z')


# x = ia.build_feed('output/ia/ia_wwi_feed.pickle', 'wwi')
# the_out_sheet.appendData(x)
x = ia.build_feed(output_folder + feed_stem + '.pickle', abbr)
the_out_sheet.appendData(x)


# fin
