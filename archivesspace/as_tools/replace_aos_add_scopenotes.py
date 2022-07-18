# Script to add scope notes to archival objects based on ref id.

import ASFunctions as asf
import json
from sheetFeeder import dataSheet
import dcps_utils as util
import os.path


SERVER = "Test"  # Test | Dev | Prod
asf.setServer(SERVER)

MY_NAME = __file__


# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)


def main():
    sheet_id = "xxxxxxxxxxxxxxxxxx"

    input_sheet = dataSheet(sheet_id, "data!A:Z")
    output_sheet = dataSheet(sheet_id, "output!A:Z")

    the_data = input_sheet.getData()

    # Uncomment this if the first row is heads to be removed.
    # the_heads = the_data.pop(0)

    output_data = []

    repo = 5  # UT

    # assuming data in format [title, ref, note]
    for row in the_data:
        refid = row[1]
        note_text = row[2]
        # get the AO by ref
        the_ao = json.loads(asf.getArchivalObjectByRef(repo, refid))
        # determine the ASID
        asid = the_ao["uri"].split("/")[4]

        new_ao = add_note(the_ao, note_text)  # TODO: write this function

        new_json = json.dumps(new_ao)
        # Post the updated AO
        post = asf.postArchivalObject(repo, asid, new_json)
        output_data.append([SERVER, repo, asid, refid, str(post)])

    # Report results
    output_sheet.appendData(output_data)


if __name__ == "__main__":
    main()
