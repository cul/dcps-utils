# Script to harvest collection-level data from AS via OAI-PMH feed, and transform into Voyager-format MARCXML for nightly overlay.

import os
import datetime
import dcps_utils as util
import argparse
import digester  # for generating composite digest of report info.


def main():
    """Script to harvest collection-level data from AS via OAI-PMH feed, and transform into Voyager-format MARCXML for nightly overlay.
    Output is (a) asRaw.xml (deltas), (b) asAllRaw.xml (all records), and (c) asClean.xml,
    transformed into Voyager MARCXML.
    Options:
    --HARVESTALL: ignore date params and get all records.
    --TEST: output to test oai directory.
    """
    p = argparse.ArgumentParser(
        description="Script to harvest collection-level data from AS via OAI-PMH feed, and transform into Voyager-format MARCXML for nightly overlay."
    )
    p.add_argument(
        "--HARVESTALL", default=False, action="store_true", help="harvest all records?"
    )
    p.add_argument(
        "--TEST", default=False, action="store_true", help="run in test mode?"
    )

    args = p.parse_args()
    print(args)

    my_name = __file__
    my_path = os.path.dirname(__file__)
    script_name = os.path.basename(my_name)

    # calculate dates in format yyyymmdd
    today = datetime.date.today().strftime("%Y%m%d")
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

    destination_folder = (
        "/cul/cul0/ldpd/archivesspace/test/oai"
        if args.TEST
        else "/cul/cul0/ldpd/archivesspace/oai"
    )

    xslt_path = os.path.join(my_path, "../xslt/cleanOAI.xsl")

    out_path_raw = os.path.join(destination_folder, today + ".asRaw.xml")
    out_path_raw_all = os.path.join(destination_folder, today + ".asAllRaw.xml")
    out_path_clean = os.path.join(destination_folder, today + ".asClean.xml")

    # Set server to Prod | Test | Dev
    server = "Prod"

    fromDate = yesterday

    # Set 'from' date to yesterday unless harvesting all
    date_params = " " if args.HARVESTALL else "-f " + yesterday

    # Harvest OAI-PMH data
    print("Harvesting data from OAI...")
    util.oai_harvest(out_path_raw, server=server, date_params=date_params)

    # Process through XSLT

    print("Processing file with XSLT...")
    x = util.saxon_process(out_path_raw, xslt_path, out_path_clean)
    print(x)
    if not args.TEST:
        digester.post_digest(script_name, x)

    print("Harvesting all records for reporting ...")
    date_params = " "
    util.oai_harvest(out_path_raw_all, server=server, date_params=date_params)

    # Remove old OAI files
    util.file_cleanup(destination_folder, 30)

    if not args.TEST:
        digester.post_digest(
            script_name,
            script_name
            + " completed at "
            + str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
            + ".",
        )


if __name__ == "__main__":
    main()
