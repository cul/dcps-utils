# TEST: Script to harvest OAI deltas and run XSLT.

import os
import datetime
import dcps_utils as util


def main():

    my_path = os.path.dirname(__file__)

    # calculate dates in format yyyymmdd
    today = datetime.date.today().strftime("%Y%m%d")
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    # destination_folder = "/cul/cul0/ldpd/archivesspace/oai"
    destination_folder = "/cul/cul0/ldpd/archivesspace/test"  # test
    # destination_folder = "./"  # test
    xslt_path = os.path.join(my_path, "cleanOAI.xsl")
    saxon_path = os.path.join(my_path, "../../resources/saxon-9.8.0.12-he.jar")
    # saxon_path = os.path.join(my_path, "../resources/saxon-9.8.0.12-he.jar")  # test

    out_path_raw = os.path.join(destination_folder, today + ".asRaw.xml")
    out_path_clean = os.path.join(destination_folder, today + ".asClean.xml")

    # Set server to Prod | Test | Dev
    server = "Prod"

    # Set to True to harvest entire set of records; otherwise, will harvest deltas since yesterday's date.
    process_all = False

    fromDate = yesterday

    if process_all == True:
        date_params = ""
    else:
        date_params = "-f " + fromDate  # + " -u " + toDate

    # Harvest OAI-PMH data
    print("Harvesting data from OAI...")
    util.oai_harvest2(out_path_raw, server=server, date_params=date_params)

    # Process through XSLT
    print("Processing file with XSLT...")
    x = util.saxon_process(saxon_path, out_path_raw, xslt_path, out_path_clean)
    print(x)


if __name__ == "__main__":
    main()
