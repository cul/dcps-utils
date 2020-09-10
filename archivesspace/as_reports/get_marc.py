# import ASFunctions as asf
# import json
from pprint import pprint
import dcps_utils as util
import time
import os.path
import csv
# from pymarc import MARCReader

my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)


the_bibids = []

# aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/bibids_by_aeon_rank_4.csv'
# aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/test.csv'
aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-batch_7.csv'

the_bibs = open(aCSV)
for row in csv.reader(the_bibs):
    the_bibids.append(row[0])
the_bibs.close()


for abib in the_bibids:
    print(abib)

    x = util.get_clio_marc(abib)

    if x:  # not returning error

        marc_path = os.path.join(my_path, 'output/marc/' + str(abib) + '.marc')

        print('saving ' + str(abib) + ' to ' + marc_path)

        with open(marc_path, 'wb') as f:
            f.write(x)

        time.sleep(10)
