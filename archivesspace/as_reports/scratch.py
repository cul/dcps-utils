import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet
import dcps_utils as util
import time
import os.path
from pymarc import MARCReader
import csv

my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

sheet_id = '1tYOXSDFlkbX_revB_ULvhmCdvKkyzpipBTkYqYXcM38'
# sheet_id = '1e43qKYvqGQFOMxA70U59yPKPs18y-k3ohRNdU-qrTH0'  # test

holdings_sheet = dataSheet(
    sheet_id, 'holdings!A:Z')


# the_bibids = [
#     7467251,
#     6093730,
#     5483040,
#     6911309,
#     # 4079581,
#     4078997,
#     4412857,
#     6621724,
#     4079192,
#     4079335,
#     10208560,
#     4078361,
#     4079169,
#     5010936,
#     6062290,
#     6607719,
#     5012632,
#     4079753,
#     4079626,
#     4078638,
#     # 4078518,
#     9489034,
#     4079015,
#     4079444,
#     4079598,
#     6910705,
#     10491409,
#     4079642,
#     7094252,
#     4078651,
#     6058659,
#     4078806,
#     4079432,
#     4079530,
#     4079544,
#     5691172,
#     4077415,
#     4079018,
#     5685745,
#     10199444,
#     4079345,
#     4079498,
#     6909494,
#     11138357,
#     8683406,
#     4078823,
#     4202865,
#     4079355,
#     4079117,
#     4079905,
#     4079917,
#     6484240,
#     4078917,
#     4078818,
#     8429461,
#     4078871,
#     4079387,
#     4078520,
#     5541450,
#     4079713,
#     4078858,
#     9364858,
#     4079112,
#     4079700,
#     12107465,
#     4078765,
#     4078928,
#     4079050,
#     4079537,
#     4078696,
#     4079625,
#     4079915,
#     4079089,
#     7341105,
#     4079136,
#     4079491,
#     9052094,
#     4079136,
#     4079350,
#     4079752,
#     4079752,
#     4078875,
#     4078866,
#     6259383,
#     5018084,
#     4079042,
#     4079099,
#     4078784,
#     7459260,
#     4078401,
#     4079356,
#     6297812,
#     10169543,
#     4079362,
#     4079514,
#     6134809,
#     4079679,
#     7748797,
#     4079451,
#     10392033
# ]


# the_bibids = [4078424,
#               4078614,
#               6297800,
#               4079728,
#               10811616,
#               4078991,
#               4078595,
#               4078837,
#               7748599,
#               4078713,
#               7089617,
#               4078512,
#               4079434,
#               10997887,
#               4079249,
#               4078945,
#               4079361,
#               4078603,
#               4078522,
#               4079559,
#               7745809,
#               4078919,
#               4079541,
#               4079881,
#               6228537,
#               4078645,
#               10101342,
#               4079170,
#               6930622,
#               6892527,
#               4078563,
#               4079659,
#               4079523,
#               4078408,
#               4079120,
#               4079154,
#               5419526,
#               8896265,
#               8960940,
#               6898059,
#               7031632,
#               5045485,
#               4079194,
#               4079685,
#               8623590,
#               5012635,
#               4078687,
#               4078910,
#               4079371,
#               4079856,
#               4078739,
#               4079171,
#               4079754,
#               4078547,
#               4078613,
#               6910494,
#               7746709,
#               4078981,
#               4079338,
#               4079482,
#               7749013,
#               4079428,
#               4079449,
#               4078904,
#               11527175,
#               4078426,
#               4079689,
#               4079732,
#               6939740,
#               9462077,
#               4077412,
#               4078541,
#               6217591,
#               4078817,
#               5419251,
#               6909763,
#               4079583,
#               4079628,
#               5710251,
#               7008843,
#               6761446,
#               4079487,
#               4079907,
#               5540444,
#               5550183,
#               7229539,
#               4079147,
#               5420146,
#               4078984,
#               6256785,
#               4079096,
#               9382776,
#               4078939,
#               4079595,
#               6262245,
#               4079209,
#               4079647,
#               4078649,
#               4079022,
#               6881813,
#               ]


the_bibids = []

aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/bibids_by_aeon_rank_1.csv'
the_bibs = open(aCSV)
for row in csv.reader(the_bibs):
    the_bibids.append(row[0])
the_bibs.close()


the_heads = ['bibid', '852$0', '852$a', '852$b', '852$h']
the_rows = [the_heads]

for abib in the_bibids:
    # x = util.get_clio_marc(abib)

    marc_path = os.path.join(my_path, 'output/marc/' + str(abib) + '.marc')

    # print(abib)

    with open(marc_path, 'rb') as f:
        reader = MARCReader(f)
        for record in reader:
            the_852s = record.get_fields('852')
            the_099 = record.get_fields('099')
            the_bibid = the_099[0].get_subfields('a')[0]
            print(the_bibid)
            # the_876s = record.get_fields('876')

            for r in the_852s:
                subs = r.get_subfields('0', 'a', 'b', 'h')
                the_rows.append([the_bibid] + subs)


print(the_rows)

holdings_sheet.clear()
x = holdings_sheet.appendData(the_rows)
print(x)
quit()
