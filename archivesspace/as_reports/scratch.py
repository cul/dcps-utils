import ASFunctions as asf
from sheetFeeder import dataSheet
import json


def main():
    # Main code goes here.

    asf.setServer("Prod")
    lookup_csv = "id_lookup_prod.csv"

    sheet_id = '1ScU8xTMt-HaiJCFWhsatPOX2fI80V0H-YLzPU7dJbwg'
    the_input_sheet = dataSheet(sheet_id, "oclc_voyager!A:Z")
    the_output_sheet = dataSheet(sheet_id, "oclc_as!A:Z")

    the_bibs = the_input_sheet.getDataColumns()[0]

    the_data = []

    for a_bib in the_bibs:

        repo, asid = asf.lookupByBibID(a_bib, lookup_csv)
        res = json.loads(asf.getResource(repo, asid))

        if "user_defined" in res:

            user_defnd = res["user_defined"]

            if "string_2" in user_defnd:
                str_2 = user_defnd["string_2"]
            else:
                str_2 = "-"

            if "string_3" in user_defnd:
                str_3 = user_defnd["string_3"]
            else:
                str_3 = "-"

            a_row = [a_bib, str_2, str_3]

        else:
            a_row = [a_bib]

        the_data.append(a_row)

    print(the_data)

    the_output_sheet.clear()
    the_output_sheet.appendData(the_data)

    quit()


# Functions go here.

if __name__ == "__main__":
    main()
