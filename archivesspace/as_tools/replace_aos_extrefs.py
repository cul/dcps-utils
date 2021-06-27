# Fix extrefs in Archival Objects. See ACFA-302.
from os import write
import dcps_utils as util
import datefinder
import datetime
import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint
import re


def main():
    SERVER = "Prod"  # test
    # SERVER = "Prod"
    asf.setServer(SERVER)

    sheet_id = '1Jbdhda0HbmHKJ7COOJ3CBzdMwpSeIbYHyXzr179ETpI'
    read_sheet = dataSheet(sheet_id, 'TEST!A:Z')  # Test
    write_sheet = dataSheet(sheet_id, 'Output!A:Z')

    the_data = read_sheet.getData()
    the_data.pop(0)

    # print(the_refs)

    the_output = []
    for r in the_data:
        repo = r[1]
        ref = r[2]
        extref_old = r[3]
        extref_new = r[5]
        the_ao = json.loads(asf.getArchivalObjectByRef(repo, ref))
        asid = the_ao['uri'].split('/')[4]

        print("asid: " + str(asid))

        the_notes = json.dumps(the_ao['notes'])

        # fix problem of leading space in href
        the_new_notes = the_notes.replace(
            'xlink:href=\\" http', 'xlink:href=\\"http')
        # replace old url with new one
        the_new_notes = the_new_notes.replace(extref_old, extref_new)

        print(the_new_notes)
        the_ao['notes'] = json.loads(the_new_notes)

        pprint(the_ao)

        x = asf.postArchivalObject(repo, asid, json.dumps(the_ao))
        out_row = [SERVER, repo, asid, ref, extref_old, extref_new, str(x)]
        print(out_row)
        the_output.append(out_row)

    # write_sheet.clear()
    write_sheet.appendData(the_output)
    quit()


# Functions go here


if __name__ == "__main__":
    main()
