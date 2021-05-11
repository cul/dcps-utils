# TESTING. Check if data updated in AS has been loaded in CLIO.
import dcps_utils as util
import random
from pymarc import MARCReader
import os
import datetime


MY_NAME = __file__
MY_PATH = os.path.dirname(__file__)
SCRIPT_NAME = os.path.basename(MY_NAME)

# calculate dates in format yyyymmdd
# TODAY = datetime.date.today().strftime("%Y%m%d")
YESTERDAY = (datetime.date.today() -
             datetime.timedelta(days=1)).strftime("%Y%m%d")

SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/oai"
XSLT_PATH = os.path.join(MY_PATH, "../xslt/bibids_as_list.xsl")
# path to yesterday's OAI output, which should have all been
# loaded yesterday by litoserv.
SOURCE_PATH = os.path.join(SOURCE_FOLDER, YESTERDAY + ".asRaw.xml")


def main():
    print(check_clio())
    quit()


def check_clio():

    # Get a list of BIBIDs from stylesheet
    x = util.saxon_process(SOURCE_PATH, XSLT_PATH, None)
    the_deltas = x.split(',')

    if len(the_deltas) < 1:
        print("No bibids found in " + str(SOURCE_PATH) + ". Bypassing CLIO check.")
        quit()

    # Check to see if the datestamp in the 005 field matches the date from the delta update.

    # Allow a couple of retries, as some MARC records are very large and
    # may not be loadable by http.
    retry_max = 2
    retries = 0
    # Choose one random one to look up
    bibid = random.choice(the_deltas)
    the_bibids_tried = []

    while retries < retry_max:

        while bibid in the_bibids_tried:
            bibid = random.choice(the_deltas)
        the_bibids_tried.append(bibid)
        # print(bibid)
        # print(retries)
        try:
            datestamp = read_005(bibid)
            if datestamp == YESTERDAY:
                return True
            print("WARNING: 005 data for " + str(bibid) +
                  " (" + datestamp + ") does not match " + str(YESTERDAY))
            return False
            # retries = retry_max
        except Exception as e:
            if "request error" in str(e):
                retries += 1
                raise Exception(
                    "CLIO error: Could not verify that datestamps have been updated! " + str(e))

    quit()


def read_005(bibid):
    marc = util.get_clio_marc(bibid)
    reader = MARCReader(marc)
    for record in reader:
        # title = record.title()
        datestamp = record['005'].value()[0:8]
    return datestamp


def test_clio_check():
    assert check_clio() == True


if __name__ == "__main__":
    main()
