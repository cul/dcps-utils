# TESTING. Check if data updated in AS has been loaded in CLIO.
import dcps_utils as util
import random
from pymarc import MARCReader
import os
import datetime


def main():

    # the_bibids = [3460558]
    # the_bibids_tried = []

    # retry_max = 2
    # retries = 0
    # bibid = random.choice(the_bibids)

    # while retries < retry_max:

    #     while bibid in the_bibids_tried:
    #         bibid = random.choice(the_bibids)
    #     the_bibids_tried.append(bibid)
    #     print(bibid)
    #     print(retries)
    #     try:
    #         datestamp = read_005(bibid)
    #         print(datestamp)
    #         retries = retry_max
    #     except Exception as e:
    #         if "request error" in str(e):
    #             retries += 1
    #             print(e)

    # quit()

    MY_NAME = __file__
    MY_PATH = os.path.dirname(__file__)
    SCRIPT_NAME = os.path.basename(MY_NAME)

    # calculate dates in format yyyymmdd
    TODAY = datetime.date.today().strftime("%Y%m%d")
    YESTERDAY = (datetime.date.today() -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")
    # YESTERDAY = "20210312"  # Test

    SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/oai"

    XSLT_PATH = os.path.join(MY_PATH, "../xslt/bibids_as_list.xsl")

    SOURCE_PATH = os.path.join(SOURCE_FOLDER, YESTERDAY + ".asRaw.xml")

    # Get a list of BIBIDs from stylesheet
    x = util.saxon_process(SOURCE_PATH, XSLT_PATH, None)
    the_deltas = x.split(',')

    if len(the_deltas) < 1:
        print("No bibids found in " + str(SOURCE_PATH) + ". Bypassing CLIO check.")
        quit()

    # Check to see if the datestamp in the 005 field matches the date from the delta update.

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
                print("OK!")
            else:
                print("WARNING: 005 data for " + str(bibid) +
                      " (" + datestamp + ") does not match " + str(YESTERDAY))
            retries = retry_max
        except Exception as e:
            if "request error" in str(e):
                retries += 1
                print(e)

    quit()


def read_005(bibid):
    marc = util.get_clio_marc(bibid)
    # if "request error" in str(marc):
    #     return marc
    reader = MARCReader(marc)
    for record in reader:
        # title = record.title()
        datestamp = record['005'].value()[0:8]
    return datestamp


if __name__ == "__main__":
    main()
