# Script to gather ids and bibids for AI assets linked from CLIO, harvest metadata from IA, and save in a pickled data file. This data then gets used to build an OPDS feed in the next step in workflow.

# internet archive python library docs:
# https://archive.org/services/docs/api/internetarchive/

import dcps_utils as util
from pprint import pprint
from datetime import datetime
from sheetFeeder import dataSheet
import ia_opds_functions as ia


def main():

    # Set these per collection before running.
    # sheet_tab = '965carnegiedpf'  # The name of the tab to read from; change this
    # # sheet_tab = 'test'  # The name of the tab to read from; change this
    # feed_stem = 'ia_ccny_feed'  # Change this
    # collection_title = "Carnegie Corporation of New York"  # Change this
    # sheet_tab = 'MWM'  # The name of the tab to read from; change this
    # feed_stem = 'ia_mwm_feed'  # Change this
    # collection_title = "Muslim World Manuscripts"  # Change this
    # sheet_tab = 'Durst'  # The name of the tab to read from; change this
    # feed_stem = 'ia_durst_feed'  # Change this
    # collection_title = "Seymour B. Durst Old York Library"  # Change this
    # sheet_tab = 'AveryTrade'  # The name of the tab to read from; change this
    # feed_stem = 'ia_avt_feed'  # Change this
    # collection_title = "Avery Library Architectural Trade Catalogs"  # Change this
    # sheet_tab = 'MedicalHeritage'  # The name of the tab to read from; change this
    # feed_stem = 'ia_med_feed'  # Change this
    # collection_title = "Medical Heritage Library"  # Change this
    sheet_tab = 'Missionary'  # The name of the tab to read from; change this
    feed_stem = 'ia_mrp_feed'  # Change this
    collection_title = "Missionary Research Pamphlets"  # Change this

    # Set the sheet to read from
    sheet_id = '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I'
    the_in_sheet = dataSheet(sheet_id, sheet_tab + '!A:Z')
    the_out_sheet = dataSheet(sheet_id, 'extract-errors!A:Z')

    pickle_path = 'output/ia/' + feed_stem + '.pickle'

    # get a list of bibids and ia ids to process
    the_inputs = the_in_sheet.getData()
    the_inputs.pop(0)  # remove head row
    the_records = []
    for i in the_inputs:
        # TODO: CHange this to get the 920s and parse them; save label (if any) for future use.
        # the_ids = i[6:]  # get arbitrary number of identifers for this row
        # rl = [{'bibid': i[0], 'id':r} for r in the_ids]
        # print(rl)
        # the_records += rl

        # the_920s = i[6:]  # get arbitrary number of 920s for this row
        the_920s = i[4].split(';')  # get arbitrary number of 920s for this row
        rl = []
        for r in the_920s:
            if 'archive.org' in r:
                rp = ia.parse_920(r)
                rl.append(
                    {'bibid': i[0], 'id': rp['id'], 'label': rp['label']})
        # rl = [{'bibid': i[0], 'id': ia.parse_920(r)['id'], 'label':ia.parse_920(r)['label']} for r in the_920s]
        the_records += rl

    # print(the_records)

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
