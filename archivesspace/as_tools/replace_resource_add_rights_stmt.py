# Script to add Metadata Rights Declarations to resources. See ACFA-298.
import ASFunctions as asf
from pprint import pprint
import json
from sheetFeeder import dataSheet


def main():
    """Bulk add metadata rights declaration value to list of resources.
    Values are defined in https://aspace.library.columbia.edu/enumerations?id=102
    See ACFA-298.
    """

    SERVER = "Prod"
    asf.setServer(SERVER)

    sheet_id = "1LPn0WRngs7i3k07VpJ_52HDRdo7FyrzfcmJX1SVtjYE"
    in_sheet = dataSheet(sheet_id, "batch")
    out_sheet = dataSheet(sheet_id, "output")

    # The statement data to be added (if there is not already one)
    md_rights_stmt = {
        # "descriptive_note": "Test Descriptive Note.",
        "file_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "jsonmodel_type": "metadata_rights_declaration",
        "license": "public_domain",
    }

    the_items = in_sheet.getData()

    the_output = []

    for item in the_items:
        repo, asid = item[0], item[1]
        result = add_md_rights_stmt(repo, asid, md_rights_stmt)
        log = [SERVER, repo, asid, result]
        the_output.append(log)

    print(the_output)

    x = out_sheet.appendData(the_output)
    print(x)
    quit()


def add_md_rights_stmt(repo, asid, md_rights_stmt):
    print(str(repo) + ":" + str(asid))
    res = json.loads(asf.getResource(repo, asid))
    if "error" in res:
        return str(res)
    if not res["metadata_rights_declarations"]:
        res["metadata_rights_declarations"].append(md_rights_stmt)
        return asf.postResource(repo, asid, json.dumps(res))
    else:
        return (
            "There is already a metadata_rights_declaration for "
            + str(repo)
            + ":"
            + str(asid)
            + "! Skipping..."
        )


if __name__ == "__main__":
    main()
