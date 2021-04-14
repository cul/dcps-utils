# TESTING. Check if data updated in AS has been loaded in CLIO.
import dcps_utils as util
import random
from pymarc import MARCReader
import os
import datetime


def main():

    MY_NAME = __file__
    MY_PATH = os.path.dirname(__file__)
    SCRIPT_NAME = os.path.basename(MY_NAME)

    # calculate dates in format yyyymmdd
    TODAY = datetime.date.today().strftime("%Y%m%d")
    YESTERDAY = (datetime.date.today() -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")
    # YESTERDAY = "20210312"  # Test

    # SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/oai"
    SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/test"  # test
    # SOURCE_FOLDER = "/Users/dwh2128/Documents/ACFA/OAI_local/20210312/"  # test
    # XSLT_PATH = os.path.join(
    #     MY_PATH, "/Users/dwh2128/Documents/ACFA/TEST/ACFA-289-test-CLIO/acfa-289-test-clio.xslt")
    XSLT_PATH = os.path.join(MY_PATH, "../xslt/bibids_as_list.xsl")
    SAXON_PATH = os.path.join(
        MY_PATH, "/opt/dcps/resources/saxon-9.8.0.12-he.jar")
    # SAXON_PATH = os.path.join(
    #     MY_PATH, '../../resources/saxon-9.8.0.12-he.jar')  # Test

    SOURCE_PATH = os.path.join(SOURCE_FOLDER, YESTERDAY + ".asRaw.xml")

    # Get a list of BIBIDs from stylesheet
    x = util.saxon_process2(SAXON_PATH, SOURCE_PATH, XSLT_PATH, None)
    the_deltas = x.split(',')

    # Choose one random one to look up
    bibid = random.choice(the_deltas)
    print(bibid)

    # Check to see if the datestamp in the 005 field matches the date from the delta update.
    datestamp = read_005(bibid)
    if datestamp == YESTERDAY:
        print("OK!")
    else:
        print("WARNING: 005 data for " + str(bibid) +
              " (" + datestamp + ") does not match " + str(YESTERDAY))

    quit()


def read_005(bibid):
    marc = util.get_clio_marc(bibid)
    reader = MARCReader(marc)
    for record in reader:
        # title = record.title()
        datestamp = record['005'].value()[0:8]
    return datestamp


if __name__ == "__main__":
    main()
