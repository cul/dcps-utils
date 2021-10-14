# Check if data updated in AS has been loaded in CLIO.
#! This is currently executed as part of pytests, not standalone.
import dcps_utils as util
import random
from pymarc import MARCReader
import os
import datetime
import requests


MY_NAME = __file__
MY_PATH = os.path.dirname(__file__)
SCRIPT_NAME = os.path.basename(MY_NAME)

# calculate dates in format yyyymmdd
TODAY = datetime.date.today().strftime("%Y%m%d")
YESTERDAY = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
DAY_BEFORE_YESTERDAY = (datetime.date.today() - datetime.timedelta(days=2)).strftime(
    "%Y%m%d"
)

SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/oai"
XSLT_PATH = os.path.join(MY_PATH, "../xslt/bibids_as_list.xsl")
# path to yesterday's OAI output, which should have all been
# loaded yesterday by litoserv.
SOURCE_PATH = os.path.join(SOURCE_FOLDER, YESTERDAY + ".asRaw.xml")


def main():

    TESTDATE = "20210718"  # test
    TESTPATH = os.path.join(SOURCE_FOLDER, TESTDATE + ".asRaw.xml")
    print(check_clio(TESTDATE, TESTPATH))

    quit()

    if is_after("20:01:01"):
        print(check_clio(TODAY, SOURCE_PATH))
    else:
        print(check_clio(YESTERDAY, SOURCE_PATH))


def is_after(cutoff_time_str):
    # cutoff_time in format "21:30:00"
    now = datetime.datetime.now().time()
    print(now)
    cutoff_time = datetime.datetime.strptime(cutoff_time_str, "%H:%M:%S")
    cutoff_time = now.replace(
        hour=cutoff_time.time().hour,
        minute=cutoff_time.time().minute,
        second=cutoff_time.time().second,
        microsecond=0,
    )
    return now > cutoff_time


def get_bibid_list(filepath, xslt_path=XSLT_PATH):
    # Get a list of BIBIDs from stylesheet
    x = util.saxon_process(filepath, XSLT_PATH, None)
    return [i for i in x.split(",") if i]  # if x is null, return null set


def check_clio(date, filepath, retry_max=2):

    the_deltas = get_bibid_list(filepath)
    print(the_deltas)

    if not the_deltas:
        print("No bibids found in " + str(filepath) + ". Bypassing CLIO check.")
        return True

    # Check to see if the datestamp in the 005 field matches the date from the delta update.

    # Allow retries, as some MARC records are very large and
    # may not be loadable by http.
    retry_max = retry_max
    retries = 0
    # Choose one random one to look up
    bibid = random.choice(the_deltas)
    print("Trying " + str(bibid) + "...")
    the_bibids_tried = []

    while retries < retry_max:

        while bibid in the_bibids_tried:
            bibid = random.choice(the_deltas)
            print("Trying " + str(bibid) + "...")
        the_bibids_tried.append(bibid)
        try:
            datestamp = read_005(bibid)
            if datestamp >= date:
                return True
            print(
                "*** WARNING: 005 data for "
                + str(bibid)
                + " ("
                + datestamp
                + ") is before "
                + str(date)
            )
            return False

        except Exception as e:
            if "request error" in str(e):
                retries += 1
    raise Exception(
        "*** ERROR: After "
        + str(retries)
        + " retries all tried BIBIDs produced http errors. "
        + str(the_bibids_tried)
    )


def read_005(bibid):
    marc = util.get_clio_marc(bibid)
    reader = MARCReader(marc)
    for record in reader:
        # title = record.title()
        datestamp = record["005"].value()[0:8]
    return datestamp


if __name__ == "__main__":
    main()
