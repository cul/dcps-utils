import ASFunctions as asf
import re
from sheetFeeder import dataSheet
import json
import os.path

# from pprint import pprint


def main():
    # Main code goes here.

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    asf.setServer("Prod")

    the_sheet = dataSheet(
        "1UQm7ffd1Kq4zqlzHZajd9YkwW1_nmOJFS1W7nI-c_Vk", "new-batch!A:Z")
    output_folder = os.path.join(my_path, "output/resource_collecting_area")

    the_rows = the_sheet.getData()
    the_new_rows = []

    the_heads = the_rows.pop(0)

    the_new_rows.append(the_heads)

    coll_area_index = 8  # the column of collecting area

    for a_row in the_rows:
        the_new_row = a_row
        # print(a_row)
        coll = ""
        repo, asid = a_row[0], a_row[1]
        if len(a_row) >= coll_area_index:
            # if there is a collecting location to add
            coll = a_row[coll_area_index]

            the_resource = asf.getResource(repo, asid)

            out_path_old = (
                output_folder + "/" + str(repo) + "_" + str(asid) + "_old.json"
            )
            out_path_new = (
                output_folder + "/" + str(repo) + "_" + str(asid) + "_new.json"
            )

            # Save copy of existing object
            print("Saving data to " + out_path_old + "....")
            with open(out_path_old, "w+") as f:
                f.write(the_resource)

            the_data = json.loads(the_resource)

            fix = False
            if "user_defined" in the_data:
                the_user_defined = the_data["user_defined"]
                if "enum_4" in the_user_defined:
                    print("Already has enum_4! Skipping.")
                else:
                    fix = True
                    the_user_defined["enum_4"] = coll
                    the_data["user_defined"] = the_user_defined
                    the_new_resource = json.dumps(the_data)

                    # Save copy of new object
                    print("Saving data to " + out_path_new + "....")
                    with open(out_path_new, "w+") as f:
                        f.write(the_new_resource)

                if fix == True:

                    try:
                        post = "[NONE]"
                        post = asf.postResource(repo, asid, the_new_resource)
                        print(post)
                    except:
                        print(
                            "Error: There was a problem posting resource "
                            + str(repo)
                            + ":"
                            + str(asid)
                            + "!"
                        )

                    the_new_row.append(coll)
            else:
                print("ERROR: No user_defined data in " +
                      str(repo) + ":" + str(asid))

        the_new_rows.append(the_new_row)

    the_sheet.clear()
    the_sheet.appendData(the_new_rows)

    # print(the_new_rows)

    quit()


# Functions go here.

if __name__ == "__main__":
    main()
