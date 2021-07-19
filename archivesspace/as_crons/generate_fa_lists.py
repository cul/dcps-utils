# Script to generate html snippets of lists of published finding aids. Run daily on cron (ldpdapp). See ACFA-213.

import dcps_utils as util
import os
from datetime import datetime, date, timedelta


def main():
    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)
    yest_str = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))

    storage_dir = "/cul/cul0/ldpd/archivesspace/"

    # XSLT for transformation. Accepts a path in param in which to save the html snippet files.

    xsl_path = os.path.join(my_path, "../xslt/generate_browse_list.xsl")

    # Use the OAI file from previous day as source to generate lists.

    input_path = storage_dir + "oai/" + yest_str + ".asAllRaw.xml"

    print("Input file: " + input_path)

    # The location for the stylesheet to save output documents.
    output_path = storage_dir + "fa_lists"
    # output_path = storage_dir + "test"  # test

    print("Output location: " + output_path)

    # output_path = os.path.join(my_path, 'output/fa_lists')  # test

    params = "output_dir=" + output_path

    # x = util.saxon_process(input_path, xsl_path, None, params)
    x = util.saxon_process(input_path, xsl_path, None, theParams=params)
    print(x)


if __name__ == "__main__":
    main()
