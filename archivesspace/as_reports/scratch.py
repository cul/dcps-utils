import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint


def main():
    # Main code goes here.

    asf.setServer("Test")

    the_sheet = dataSheet('1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Sheet1!A:Z')

    the_data = the_sheet.getData()
    the_heads = the_data.pop(0)

    for r in the_data:
        the_ref = r[2]
        lookup = json.loads (asf.getResponse('repositories/2/find_by_id/archival_objects?ref_id[]=' + the_ref))

        archival_object_uri = lookup["archival_objects"][0]["ref"]
        asid = archival_object_uri.split("/")[-1]

        ao = json.loads(asf.getArchivalObject(2,asid))
        print(','.join([the_ref,asid,ao['title']]))
    # pprint(ao)


    # aoref = '21849d537360a6da5b6d900cf561f99f'
    # aoid = asf.getArchivalObjectByRef(2, aoref)
    # print(aoid)
    # deletion = asf.deleteArchivalObject(2, aoid)
    quit()


# Functions go here.

if __name__ == "__main__":
    main()
