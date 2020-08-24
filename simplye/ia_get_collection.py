# Script to gather ids and bibids for AI assets linked from CLIO, harvest metadata from IA, and save in a pickled data file. This data then gets used to build an OPDS feed in the next step in workflow.

# internet archive python library docs:
# https://archive.org/services/docs/api/internetarchive/

import dcps_utils as util
from pprint import pprint
from datetime import datetime
from sheetFeeder import dataSheet
import ia_opds_functions as ia


def main():

    feed_stem = 'ia_avt_feed'  # Change this
    collection_title = "Avery Library Architectural Trade Catalogs"  # Change this

    # Set the correct sheet to read from
    the_in_sheet = dataSheet(
        '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'AveryTrade!A:Z')  # Change this
    the_out_sheet = dataSheet(
        '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'extract-errors!A:Z')

    pickle_path = 'output/ia/' + feed_stem + '.pickle'

    # get a list of bibids and ia ids to process
    the_inputs = the_in_sheet.getData()
    the_inputs.pop(0)  # remove head row
    the_records = []
    for i in the_inputs:
        the_ids = i[6:]  # get arbitrary number of identifers for this row
        rl = [{'bibid': i[0], 'id':r} for r in the_ids]
        print(rl)
        the_records += rl

    feed_data = ia.extract_data(the_records, feed_stem, collection_title)

    print('Saving ' + str(len(feed_data['data'])
                          ) + ' records to ' + pickle_path)
    util.pickle_it(feed_data['data'], pickle_path)

    # pprint(feed_data['data'])
    # pprint(feed_data['errors'])

    the_out_sheet.appendData(feed_data['errors'])

    # fin


if __name__ == "__main__":
    main()
