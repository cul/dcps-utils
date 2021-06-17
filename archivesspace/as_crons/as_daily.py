# Script to harvest OAI (all) and extract and clean up the deltas and via XSLT. Results are saved to /cul/cul0/ldpd/archivesspace/oai for Voyager nightly overlay.

import os
import datetime
import dcps_utils as util
# from as_reports_param import time_offset
import digester  # for generating composite digest of report info.


def main():

    # Set to True to harvest complete set; otherwise will select based on date.
    HARVESTALL = False

    my_name = __file__
    my_path = os.path.dirname(__file__)
    script_name = os.path.basename(my_name)

    # calculate dates in format yyyymmdd
    today = datetime.date.today().strftime("%Y%m%d")
    yesterday = (datetime.date.today() -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")

    destination_folder = "/cul/cul0/ldpd/archivesspace/oai"
    # destination_folder = "/cul/cul0/ldpd/archivesspace/test"  # test
    # destination_folder = "./"  # test
    xslt_path = os.path.join(my_path, "../xslt/cleanOAI.xsl")

    out_path_raw = os.path.join(destination_folder, today + ".asRaw.xml")
    out_path_raw_all = os.path.join(
        destination_folder, today + ".asAllRaw.xml")
    out_path_clean = os.path.join(destination_folder, today + ".asClean.xml")

    # Set server to Prod | Test | Dev
    server = "Prod"

    fromDate = yesterday

    # # Not using date, get all records and then filter with the XSLT!
    # date_params = ""

    # Select date interval for harvest
    # TODO: change this to be controlled by param file.

    if HARVESTALL == True:
        date_params = " "  # Use this to harvest all records.
    else:
        date_params = "-f " + yesterday

    # Harvest OAI-PMH data
    print("Harvesting data from OAI...")
    util.oai_harvest(out_path_raw, server=server, date_params=date_params)

    # Process through XSLT

    # TODO: change xsl to not require this param, if we are doing it in the harvest!
    time_offset = 'P800DT30H'

    saxon_params = " time_offset=" + time_offset

    print("Processing file with XSLT...")
    x = util.saxon_process(out_path_raw,
                           xslt_path, out_path_clean, theParams=saxon_params)
    print(x)
    digester.post_digest(script_name, x)

    print("Harvesting all records for reporting ...")
    date_params = " "
    util.oai_harvest(out_path_raw_all, server=server, date_params=date_params)

    digester.post_digest(script_name, script_name + ' completed at ' +
                         str(datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')) + '.')


if __name__ == "__main__":
    main()
