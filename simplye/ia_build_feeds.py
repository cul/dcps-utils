import ia_opds_functions as ia
from pprint import pprint
import dcps_utils as util
from sheetFeeder import dataSheet


# the_out_sheet = dataSheet(
#     '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'errors!A:Z')

# x = ia.build_feed('output/ia/ia_med_feed.pickle', 'med')
# the_out_sheet.appendData(x)

# the_out_sheet = dataSheet(
#     '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'errors!A:Z')

# x = ia.build_feed('output/ia/ia_avt_feed.pickle', 'avt')
# the_out_sheet.appendData(x)

the_out_sheet = dataSheet(
    '1yTDyd5GQFEsVBiKOnt5T1ejBdXhxhmXVUn6jQ-dg_5I', 'errors!A:Z')

x = ia.build_feed('output/ia/ia_wwi_feed.pickle', 'wwi')
the_out_sheet.appendData(x)

quit()
