import dcps_utils as util
from sheetFeeder import dataSheet
import ASFunctions as asf
import json


def main():

    # AS Server Dev|Prod|Test
    SERVER = "Test"
    asf.setServer(SERVER)

    # Google sheet classes
    SHEET_ID = "1twflEyc0OKWqEGV_IWv_NXWczPQMRItyCxqGqp6z5WQ"
    input_sheet = dataSheet(SHEET_ID, "Batch!A:Z")
    output_sheet = dataSheet(SHEET_ID, "Output!A:Z")

    # dict of notes per repo
    notes = {
        "RBML": "Materials may have been added to the collection since this finding aid was prepared. Contact rbml@columbia.edu for more information.",
        "STARR": "Materials may have been added to the collection since this finding aid was prepared. Contact starr@library.columbia.edu for more information.",
        "UA": "Materials have been added to the collection since this finding aid was prepared. Contact uarchives@columbia.edu for more information.",
    }

    # Build the new note
    accrual_note = {
        "jsonmodel_type": "note_multipart",
        "publish": True,
        "subnotes": [
            {
                "content": notes["RBML"],  # Change this value for other repos!
                "jsonmodel_type": "note_text",
                "publish": True,
            }
        ],
        "type": "accruals",
    }

    # assemble output for reporting in this list
    the_output = []

    # pull in batch of repos/ids from sheet
    records = input_sheet.getData()
    the_heads = records.pop(0)  # delete heads

    for r in records:
        # repo id and AS uid of record.
        repo, asid = r[0], r[1]
        # do the thing
        response = add_note(repo, asid, accrual_note)
        row = [SERVER, repo, asid, response]
        the_output.append(row)

    # write to Gsheet
    output_sheet.appendData(the_output)
    quit()


def add_note(repo, asid, note):
    # Fn to GET resource, add note, and POST
    # pull down resource
    resource = json.loads(asf.getResource(repo, asid))
    # TODO: add error trapping in case there is no record returned?
    resource["notes"].append(note)
    # return the API response
    return asf.postResource(repo, asid, json.dumps(resource))


if __name__ == "__main__":
    main()
