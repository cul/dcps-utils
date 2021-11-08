import dcps_utils as util
from sheetFeeder import dataSheet
import ASFunctions as asf
import json


def main():

    SERVER = "Dev"
    asf.setServer(SERVER)

    SHEET_ID = "1twflEyc0OKWqEGV_IWv_NXWczPQMRItyCxqGqp6z5WQ"
    output_sheet = dataSheet(SHEET_ID, "Output!A:Z")

    notes = {
        "RBML": "Materials may have been added to the collection since this finding aid was prepared. Contact rbml@columbia.edu for more information.",
        "STARR": "Materials may have been added to the collection since this finding aid was prepared. Contact starr@library.columbia.edu for more information.",
        "UA": "Materials have been added to the collection since this finding aid was prepared. Contact uarchives@columbia.edu for more information.",
    }

    accrual_note = {
        "jsonmodel_type": "note_multipart",
        "publish": True,
        "subnotes": [
            {
                "content": notes["RBML"],
                "jsonmodel_type": "note_text",
                "publish": True,
            }
        ],
        "type": "accruals",
    }

    the_output = []

    the_sheet = dataSheet(SHEET_ID, "Batch!A:Z")

    records = the_sheet.getData()
    the_heads = records.pop(0)

    for r in records:
        repo, asid = r[0], r[1]
        response = add_note(repo, asid, accrual_note)
        row = [SERVER, repo, asid, response]
        the_output.append(row)

    output_sheet.appendData(the_output)
    quit()


def add_note(repo, asid, note):
    resource = json.loads(asf.getResource(repo, asid))
    resource["notes"].append(note)
    return asf.postResource(repo, asid, json.dumps(resource))


if __name__ == "__main__":
    main()
