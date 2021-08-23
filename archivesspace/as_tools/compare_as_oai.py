# Script to harvest OAI from Prod and Dev with different versions of AS, and generate
# files with overlapping records to diff.
# After harvesting data from Prod and Dev, parameters of file locations (inputs and outpus)
# are passed to XSLT. Results will be found in destination_folder path.
# Diff the resulting files to see changes in output for unchanged records between
# two versions of AS.
# (If running locally, change folder location accordingly.)

import os
import datetime
import dcps_utils as util


MY_NAME = __file__
MY_PATH = os.path.dirname(__file__)


def main():

    destination_folder = "/cul/cul0/ldpd/archivesspace/test/oai"  # test
    xslt_path = os.path.join(MY_PATH, "../xslt/as_compare_oai.xsl")

    # date_params = " "  # Use this to harvest all records.
    date_params = "-u 20200101"

    today = datetime.date.today().strftime("%Y%m%d")
    prod_harvest_path = os.path.join(destination_folder, today + ".asPROD.xml")
    prod_diff_path = os.path.join(destination_folder, today + ".diff_prod.xml")
    dev_harvest_path = os.path.join(destination_folder, today + ".asDEV.xml")
    dev_diff_path = os.path.join(destination_folder, today + ".diff_dev.xml")

    # Harvest from Prod
    print("Harvesting Prod data to " + prod_harvest_path)
    util.oai_harvest(prod_harvest_path, server="Prod", date_params=date_params)

    print(" ")
    # Harvest from Dev
    print("Harvesting Dev data to " + dev_harvest_path)
    util.oai_harvest(dev_harvest_path, server="Dev", date_params=date_params)

    print(" ")

    saxon_params = (
        " prodFile="
        + prod_harvest_path
        + " devFile="
        + dev_harvest_path
        + " prodOutFile="
        + prod_diff_path
        + " devOutFile="
        + dev_diff_path
    )

    print(saxon_params)

    print("Generating diff files with XSLT...")
    x = util.saxon_process(xslt_path, xslt_path, outFile=None, theParams=saxon_params)
    print(x)

    quit()


if __name__ == "__main__":
    main()
