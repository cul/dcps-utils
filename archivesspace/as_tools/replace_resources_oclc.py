# Script to take a delimited file of format:
#   bibid|string_2|string_3
# and feed the OCLC strings into the user_defined fields
# in ArchivesSpace.
import ASFunctions as asf
import csv
import json


def main():
    # Main code goes here.

    asf.setServer("Prod")

    lookup_csv = "id_lookup_prod.csv"
    id_file = "/Users/dwh2128/Documents/ACFA/TEST/ACFA-226-oclc/035s_20200915.txt"

    # Read a list of bibids and oclc strings
    the_data = []
    with open(id_file) as ids:
        for row in csv.reader(ids, delimiter="|"):
            the_data.append([row[0], row[1], row[2]])

    for a_row in the_data:
        bibid = a_row[0]
        print(bibid)
        str_2 = a_row[1]
        str_3 = a_row[2]
        try:
            repo, asid = asf.lookupByBibID(bibid, lookup_csv)

            x = asf.getResource(repo, asid)
            y = json.loads(x)

            user_defnd = y["user_defined"] if "user_defined" in y else {}
            user_defnd["string_2"] = str_2
            user_defnd["string_3"] = str_3

            print(user_defnd)

            y["user_defined"] = user_defnd

            z = json.dumps(y)
            post = asf.postResource(repo, asid, z)
            print(post)

        except Exception as e:
            print(e + ": Could not lookup " + str(bibid))

    # print(new_data)


# Functions go here.

if __name__ == "__main__":
    main()
