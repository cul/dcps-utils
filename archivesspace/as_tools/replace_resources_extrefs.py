# Fix extrefs in Archival Objects. See ACFA-302.
from os import write, path
import dcps_utils as util
import datefinder
import datetime
import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint
import re


def main():
    # SERVER = "Test"  # test
    SERVER = "Prod"
    asf.setServer(SERVER)

    LOOKUP = '/Users/dwh2128/Documents/git/dcps-utils/archivesspace/as_reports/id_lookup_prod.csv'

    sheet_id = '1Jbdhda0HbmHKJ7COOJ3CBzdMwpSeIbYHyXzr179ETpI'
    read_sheet = dataSheet(sheet_id, 'TEST!A:Z')  # Test
    write_sheet = dataSheet(sheet_id, 'Output!A:Z')

    the_data = read_sheet.getData()
    the_data.pop(0)

    # print(the_refs)

    the_output = []
    for r in the_data:
        bibid = r[0]
        repo = r[1]
        ref = r[2]
        extref_old = r[3]
        extref_new = r[5]
        the_res = json.loads(asf.getResourceByBibID(bibid, LOOKUP))
        # pprint(the_res)

        asid = the_res['uri'].split('/')[4]

        print("repo: " + str(repo) + "; asid: " + str(asid))

        the_notes = json.dumps(the_res['notes'])
        # print(the_notes)
        print(" ")

        the_new_notes = replace_notes(
            the_notes, [
                # fix problem of leading space in href
                {'find': 'xlink:href=\\" http',
                 'replace': 'xlink:href=\\"http'},
                # replace old url with new one
                {'find': extref_old,
                 'replace': extref_new}])

        # print(the_new_notes)

        the_res['notes'] = json.loads(the_new_notes)

        x = asf.postResource(repo, asid, json.dumps(the_res))
        out_row = [SERVER, repo, asid, ref, extref_old, extref_new, str(x)]
        print(out_row)
        the_output.append(out_row)

    # # write_sheet.clear()
    write_sheet.appendData(the_output)
    quit()


def replace_notes(notes_json, replacements):
    # replacements = [{'find': 'str1', 'replace': 'str2'},...]
    the_new_notes = notes_json
    for r in replacements:
        the_new_notes = the_new_notes.replace(r['find'], r['replace'])
    return the_new_notes


if __name__ == "__main__":
    main()
