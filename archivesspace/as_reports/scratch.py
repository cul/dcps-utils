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

    repo = 2
    asid = 4851

    the_query = '/repositories/' + \
        str(repo) + '/resources/' + str(asid) + '/top_containers'

    x = asf.getResponse(the_query)

    for r in x:
        print('Getting data for ' + r['ref'])
        x = asf.getResponse(r['ref'])
        pprint(x)


if __name__ == "__main__":
    main()
