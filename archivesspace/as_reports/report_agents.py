import ASFunctions as asf
import json
import os.path
import pickle
from pprint import pprint
from sheetFeeder import dataSheet
import dpath.util


my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

sheet_id = "1dTeMAK_cGWAUvrqvAiY2hGy4gJewrmWjnuIZu8NhWwE"

# List of fields to extract, expressed as dpaths.
the_fields = [
    ["uri", "uri"],
    ["title", "title"],
    ["source", "names/0/source"],
    ["authority_id", "names/0/authority_id"],
    ["is_linked_to_published_record", "is_linked_to_published_record"],
    ["publish", "publish"],
]


family_agents_file = os.path.join(my_path, "output/agents_families.pickle")
corp_agents_file = os.path.join(my_path, "output/agents_corporate.pickle")
persons_agents_file = os.path.join(my_path, "output/agents_persons.pickle")


the_stuff = [
    {
        "name": "families",
        "sheet": dataSheet(sheet_id, "families!A:Z"),
        "pickle": family_agents_file,
    },
    {
        "name": "corporate",
        "sheet": dataSheet(sheet_id, "corporate!A:Z"),
        "pickle": corp_agents_file,
    },
    {
        "name": "persons",
        "sheet": dataSheet(sheet_id, "persons!A:Z"),
        "pickle": persons_agents_file,
    },
]

for i in the_stuff:
    the_sheet = i["sheet"]
    # open pickled file
    with open(i["pickle"], "rb") as f:
        agent_data = pickle.load(f)

    the_heads = [x[0] for x in the_fields]
    the_output = [the_heads]

    for agent in agent_data:
        the_row = []
        # Use dpath to extract values from dict and compose into rows.
        for af in the_fields:
            try:
                d = str(dpath.util.get(agent, af[1]))
            except:
                d = ""
            the_row.append(d)
        # print(the_row)
        the_output.append(the_row)

    the_sheet.clear()
    save = the_sheet.appendData(the_output)
    print(save)
