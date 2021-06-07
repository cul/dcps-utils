# Fix begin dates in Archival Objects. See ACFA-281.
from os import write
import dcps_utils as util
import datefinder
import datetime
import ASFunctions as asf
from sheetFeeder import dataSheet
import json
from pprint import pprint


def main():
    # SERVER = "Test" # test
    SERVER = "Prod"
    asf.setServer(SERVER)

    sheet_id = '1OABHEJF1jqA1vlbW5yTENry5W7YqKlag5nJDJ9ouCzg'
    # read_sheet = dataSheet(sheet_id, 'Test!A:Z')  # Test
    read_sheet = dataSheet(sheet_id, 'Prod!A:Z')  # Test
    write_sheet = dataSheet(sheet_id, 'output!A:Z')

    the_refs = read_sheet.getDataColumns()[0]
    # print(the_refs)

    the_output = []
    for r in the_refs:
        the_ao = json.loads(asf.getArchivalObjectByRef(2, r))
        asid = the_ao['uri'].split('/')[4]
        old_date = str(the_ao['dates'][0]['begin'])
        new_ao = fix_begin_date(2, the_ao)
        new_date = str(new_ao['dates'][0]['begin'])
        print("asid: " + str(asid))
        x = asf.postArchivalObject(2, asid, json.dumps(new_ao))
        out_row = [SERVER, r, asid, old_date, new_date, str(x)]
        # print(out_row)
        the_output.append(out_row)

    write_sheet.clear()
    write_sheet.appendData(the_output)
    quit()

    x = fix_begin_date(2, 'b2ec9ce511e4212ebb145fb909ca85bd')
    print(x)

    pprint(json.loads(asf.getArchivalObjectByRef(
        2, 'b2ec9ce511e4212ebb145fb909ca85bd')))
    quit()


# Functions go here


def datetime_to_date(str):
    x = datefinder.find_dates(str)
    for m in x:
        # return the first date found (should be only one)
        return m.strftime('%Y-%m-%d')


def fix_begin_date(repo, ao_data):
    the_dates = ao_data['dates']
    begin_date = the_dates[0]['begin']
    print("Original: " + str(begin_date))
    new_date = datetime_to_date(begin_date)
    print("New: " + str(new_date))
    the_dates[0]['begin'] = new_date
    ao_data['dates'] = the_dates

    # return asf.postArchivalObject(repo, asid, json.dumps(the_data))
    return ao_data


if __name__ == "__main__":
    main()
