import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint
import requests
import os
import dcps_utils as util


def main():
    # Main code goes here.
    my_path = os.path.dirname(__file__)

    xml_path = os.path.join(my_path, '../xslt/EAD_SAMPLE.xml')
    schema_path = os.path.join(my_path, "../schemas/cul_as_ead.rng")

    x = util.jing_process(xml_path, schema_path)

    print(x)
    quit()
    asf.setServer("Test")

    x = asf.getResource(2, 4967)
    pprint(json.loads(x))
    quit()

    the_sheet = dataSheet(
        '1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Test!A:Z')  # Test
    # the_sheet = dataSheet('1IdaoISdS_n0Hf_s_JTvE85QgMa4tBdoAIULzb6wk_-w', 'Sheet1!A:Z')

    the_data = the_sheet.getData()
    the_heads = the_data.pop(0)

    for r in the_data:
        the_ref = r[2]
        asid = get_ao_asid_from_ref(2, the_ref)

        print(','.join([the_ref, asid]))

        deletion = asf.deleteArchivalObject(2, asid)
        print(deletion)
        print(type(deletion))

    quit()


# Functions go here.

def get_ao_asid_from_ref(repo, ref):
    lookup = json.loads(asf.getResponse(
        'repositories/' + str(repo) + '/find_by_id/archival_objects?ref_id[]=' + ref))
    uri = lookup["archival_objects"][0]["ref"]
    return uri.split("/")[-1]


if __name__ == "__main__":
    main()
