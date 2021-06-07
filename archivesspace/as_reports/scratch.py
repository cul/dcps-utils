import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint
import requests
import os
import dcps_utils as util
import datefinder
import datetime


def datetime_to_date(str):
    x = datefinder.find_dates(str)
    for m in x:
        # return the first date found (should be only one)
        return m.strftime('%Y-%m-%d')


def fix_begin_date(repo, refid):
    the_data = json.loads(asf.getArchivalObjectByRef(
        repo, refid))
    asid = the_data['uri'].split('/')[4]
    print("asid: " + str(asid))
    the_dates = the_data['dates']
    begin_date = the_dates[0]['begin']
    print("Original: " + str(begin_date))
    new_date = datetime_to_date(begin_date)
    print("New: " + str(new_date))
    the_dates[0]['begin'] = new_date
    the_data['dates'] = the_dates

    return asf.postArchivalObject(repo, asid, json.dumps(the_data))


def main():
    # Main code goes here.

    asf.setServer("Test")

    x = fix_begin_date(2, 'b2ec9ce511e4212ebb145fb909ca85bd')
    print(x)

    pprint(json.loads(asf.getArchivalObjectByRef(
        2, 'b2ec9ce511e4212ebb145fb909ca85bd')))
    quit()

    the_sheet = dataSheet(
        '1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Test!A:Z')  # Test
    # the_sheet = dataSheet('1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Sheet1!A:Z')

    the_data = the_sheet.getData()
    the_heads = the_data.pop(0)

    for r in the_data:
        the_ref = r[2]
        asid = get_ao_asid_from_ref(2, the_ref)

        print(','.join([the_ref, asid]))

        deletion = asf.deleteArchivalObject(2, asid)
        print(deletion)
        print(type(deletion))

    quit()


# Functions go here.

def get_ao_asid_from_ref(repo, ref):
    lookup = json.loads(asf.getResponse(
        'repositories/' + str(repo) + '/find_by_id/archival_objects?ref_id[]=' + ref))
    uri = lookup["archival_objects"][0]["ref"]
    return uri.split("/")[-1]


if __name__ == "__main__":
    main()
