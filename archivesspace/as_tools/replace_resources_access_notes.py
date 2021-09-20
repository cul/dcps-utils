import dcps_utils as util
from sheetFeeder import dataSheet
import ASFunctions as asf
import json
from pprint import pprint


def main():
    """Add generic condition of access note to collections in RBML Books. See ACFA-320."""

    data_sheet = dataSheet("1DogTcXuuGXxbgWNVFbwaSXcVEtil69yKw-E_n8QGX4E", "Batch!A:Z")
    out_sheet = dataSheet("1DogTcXuuGXxbgWNVFbwaSXcVEtil69yKw-E_n8QGX4E", "Output!A:Z")

    # add access conditions note for all RBML BOOKS
    new_note = {
        "jsonmodel_type": "note_multipart",
        "publish": True,
        "rights_restriction": {"local_access_restriction_type": []},
        "subnotes": [
            {
                "content": "All books in this collection are cataloged, and should be requested individually in CLIO. This record is for informational purposes only.",
                "jsonmodel_type": "note_text",
                "publish": True,
            }
        ],
        "type": "accessrestrict",
    }

    asf.setDebug(True)
    SERVER = "Prod"
    asf.setServer(SERVER)

    the_records = data_sheet.getData()
    # the_records.pop(0)

    output = []
    for r in the_records:
        repo = r[0]
        asid = r[1]
        print(asid)

        x = json.loads(asf.getResource(repo, asid))
        x["notes"].append(new_note)
        # pprint(x["notes"])

        res = asf.postResource(repo, asid, json.dumps(x))

        out_row = [SERVER, repo, asid, str(res)]
        print(out_row)
        output.append(out_row)

    out_sheet.appendData(output)

    quit()


# Functions go here


if __name__ == "__main__":
    main()
