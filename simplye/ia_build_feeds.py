import ia_opds_functions as ia
from pprint import pprint
import dcps_utils as util
from sheetFeeder import dataSheet


# the_out_sheet = dataSheet(
#     '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'errors!A:Z')

# x = ia.build_feed('output/ia/ia_med_feed.pickle', 'med')
# the_out_sheet.appendData(x)

the_out_sheet = dataSheet(
    '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'errors!A:Z')

x = ia.build_feed('output/ia/ia_avt_feed.pickle', 'avt')
the_out_sheet.appendData(x)

quit()

# feed_stem = 'ia_durst_feed'
# collection_title = "Durst"
# # collection_title = "Muslim World Manuscripts"

# recs = [{'bibid': '10299829', 'id': 'cu31924028832941'},
#         {'bibid': '10300028', 'id': 'cu31924024896957'}]

# x = ia.extract_data(recs, feed_stem, collection_title)
# pprint(x['errors'])
# pprint(x['data'])

# # Build Ling Long
# ia.build_feed('output/ia/ll/ia_ll_1931.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1932.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1933.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1933.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1934.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1935.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1936.pickle', 'll')
# ia.build_feed('output/ia/ll/ia_ll_1937.pickle', 'll')

quit()

feed_stem = 'ia_durst_feed'
collection_title = "Durst"
collection_title = "Seymour B. Durst Old York Library"

# recs = [{'bibid': '10299829', 'id': 'cu31924028832941'},
#         {'bibid': '10300028', 'id': 'cu31924024896957'}]

x = ia.extract_data(recs, feed_stem, collection_title)
pprint(x['errors'])
pprint(x['data'])
