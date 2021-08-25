import ASFunctions as asf

# from sheetFeeder import dataSheet
import json
from pprint import pprint
import requests
import os

# import dcps_utils as util
import datefinder
import datetime
from shutil import copyfile


def datetime_to_date(str):
    x = datefinder.find_dates(str)
    for m in x:
        # return the first date found (should be only one)
        return m.strftime("%Y-%m-%d")


def fix_begin_date(repo, refid):
    the_data = json.loads(asf.getArchivalObjectByRef(repo, refid))
    asid = the_data["uri"].split("/")[4]
    print("asid: " + str(asid))
    the_dates = the_data["dates"]
    begin_date = the_dates[0]["begin"]
    print("Original: " + str(begin_date))
    new_date = datetime_to_date(begin_date)
    print("New: " + str(new_date))
    the_dates[0]["begin"] = new_date
    the_data["dates"] = the_dates

    return asf.postArchivalObject(repo, asid, json.dumps(the_data))


def make_dated_backup(filepath, date):
    # make a copy of file in same directory with date prepended.
    dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    newpath = os.path.join(dir, str(date) + "_" + filename)
    return copyfile(filepath, newpath)


def main():
    # Main code goes here.

    quit()


# Functions go here.


def get_ao_asid_from_ref(repo, ref):
    lookup = json.loads(
        asf.getResponse(
            "repositories/" + str(repo) + "/find_by_id/archival_objects?ref_id[]=" + ref
        )
    )
    uri = lookup["archival_objects"][0]["ref"]
    return uri.split("/")[-1]


if __name__ == "__main__":
    main()
