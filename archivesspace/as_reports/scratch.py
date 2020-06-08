import ASFunctions as asf
from pymarc import MARCReader
import os
import json
from pprint import pprint
from sheetFeeder import dataSheet
import dcps_utils as util
import csv


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    the_bibids = []
    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/acfa-206-single-holdings_TEST.csv' # test
    aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-206-add-barcodes/bibids_by_aeon_rank_1.csv'

    the_bibs = open(aCSV)
    for row in csv.reader(the_bibs):
        the_bibids.append(row[0])
    the_bibs.close()

    # print(the_bibids)

    ### MARC ###

    # Read the MARC

    the_heads = ['bibid', 'display_string', '876$0', '876$a', '876$p']
    the_rows = [the_heads]

    for abib in the_bibids:
        print('Getting MARC for ' + str(abib))

        marc_path = os.path.join(my_path, 'output/marc/' + str(abib) + '.marc')

        with open(marc_path, 'rb') as fh:
            reader = MARCReader(fh)
            for record in reader:
                the_852s = record.get_fields('852')

                if len(the_852s) > 1:
                    print("YESSSSS!")
                    print(len(the_852s))
                    for r in the_852s:
                        # Need to specify order of subfields explicitly
                        the_852_data = [
                            r.get_subfields('0'),
                            r.get_subfields('a'),
                        ]

                        print(the_852_data)


if __name__ == "__main__":
    main()
