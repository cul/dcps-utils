import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint
import requests


def main():
    # Main code goes here.

    asf.setServer("Test")

    the_sheet = dataSheet('1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Test!A:Z') # Test
    # the_sheet = dataSheet('1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Sheet1!A:Z')

    the_data = the_sheet.getData()
    the_heads = the_data.pop(0)

    for r in the_data:
        the_ref = r[2]
        asid = get_ao_asid_from_ref(2,the_ref)

        print(','.join([the_ref,asid]))

        deletion = asf.deleteArchivalObject(2,asid)
        print(deletion)
        print(type(deletion))

    quit()


# Functions go here.

def get_ao_asid_from_ref(repo, ref):
    lookup = json.loads (asf.getResponse('repositories/' + str(repo) + '/find_by_id/archival_objects?ref_id[]=' + ref))
    uri = lookup["archival_objects"][0]["ref"]
    return uri.split("/")[-1]


if __name__ == "__main__":
    main()
