# Script to harvest OAI from Prod and Dev with different versions of AS, and generate
# files with overlapping records to diff.

import os
import datetime
import dcps_utils as util


def main():

    destination_folder = "/cul/cul0/ldpd/archivesspace/test/oai"  # test

    # date_params = " "  # Use this to harvest all records.
    date_params = "-u 20190101 "

    today = datetime.date.today().strftime("%Y%m%d")
    prod_output_path = os.path.join(destination_folder, today + ".asPROD.xml")
    dev_output_path = os.path.join(destination_folder, today + ".asDEV.xml")

    # Harvest from Prod
    print("Harvesting Prod data to " + prod_output_path)
    util.oai_harvest(prod_output_path, server="Prod", date_params=date_params)

    print(" ")
    # Harvest from Dev
    print("Harvesting Dev data to " + dev_output_path)
    util.oai_harvest(dev_output_path, server="Dev", date_params=date_params)

    quit()


if __name__ == "__main__":
    main()
