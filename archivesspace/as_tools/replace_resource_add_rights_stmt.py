# Script to add Metadata Rights Declarations to resources. See ACFA-298.
import ASFunctions as asf
from pprint import pprint
import json


def main():

    SERVER = "Dev"
    asf.setServer(SERVER)

    # The statement data to be added (if there is not already one)
    md_rights_stmt = {
        # "descriptive_note": "Test Descriptive Note.",
        "file_uri": "https://creativecommons.org/publicdomain/zero/1.0/",
        "jsonmodel_type": "metadata_rights_declaration",
        # "last_verified_date": "2021-10-19 00:00:00 " "UTC",
        "license": "public_domain",
    }

    # Testing

    repo = 2
    asid = 6337

    x = add_md_rights_stmt(repo, asid, md_rights_stmt)
    print(x)

    y = asf.getResource(repo, asid)
    pprint(json.loads(y)["metadata_rights_declarations"])

    quit()


def add_md_rights_stmt(repo, asid, md_rights_stmt):
    res = json.loads(asf.getResource(repo, asid))
    if not res["metadata_rights_declarations"]:
        res["metadata_rights_declarations"].append(md_rights_stmt)
        return asf.postResource(repo, asid, json.dumps(res))
    else:
        print(
            "There is already a metadata_rights_declaration for "
            + str(repo)
            + ":"
            + str(asid)
            + "! Skipping..."
        )


if __name__ == "__main__":
    main()
