# Script to add authorities or make other changes to agents. See ACFA-300.

import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet
import os.path


SERVER = "Prod"
# SERVER = "Test"  # test
asf.setServer(SERVER)

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)


def main():

    # x = asf.getAgent(9741, agent_type="people")
    # pprint(json.loads(x))
    # quit()

    sheet_id = "1zMJBffHe6H5EqNzGgX85ce2i5wvwck6PmQA7gJq1k4E"

    # list_sheet = dataSheet(sheet_id, 'Test!A:Z')  # test
    list_sheet = dataSheet(sheet_id, "batch!A:Z")
    report_sheet = dataSheet(sheet_id, "output!A:Z")

    the_data = list_sheet.getData()
    # the_uris = list_sheet.getDataColumns()[0]

    output_data = []
    for row in the_data:
        asid = row[0].split("/")[3]
        type = row[0].split("/")[2]  # people | corporate_entities
        try:
            auth_id = row[2]
            auth_id_uri = "http://id.loc.gov/authorities/names/" + auth_id
        except:
            auth_id_uri = ""
        print(asid)
        print(type)
        # print(auth_id_uri)
        if auth_id_uri:
            try:
                x = fix_agent(asid, type, auth_id_uri)
                pprint(x["display_name"])
                res = asf.postAgent(asid, json.dumps(x), agent_type=type)
            except agentError:
                res = "Error: Could not find agent " + str(asid) + "!"
        else:
            res = "Error: No authority ID!"
        # print(res)
        row = [SERVER, asid, type, auth_id_uri, str(res)]
        output_data.append(row)

    print(output_data)

    report_sheet.appendData(output_data)

    quit()


class agentError(Exception):
    pass


def fix_agent(asid, agent_type, authority_uri):
    x = json.loads(asf.getAgent(asid, agent_type=agent_type))
    if "error" in x:
        raise agentError("My hovercraft is full of eels")
    # print(x)

    for name in x["names"]:
        print(name)
        if name["is_display_name"] == True:
            name["authority_id"] = authority_uri
            name["source"] = "naf"

    x["display_name"]["authority_id"] = authority_uri
    x["display_name"]["source"] = "naf"

    return x


if __name__ == "__main__":
    main()
