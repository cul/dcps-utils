import dcps_utils as util
import os
from datetime import datetime, date, timedelta


def main():
    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)
    yest_str = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))

    storage_dir = "/cul/cul0/ldpd/archivesspace/"

    saxon_path = os.path.join(my_path, '../../resources/saxon-9.8.0.12-he.jar')
    xsl_filename = 'generate_browse_list.xsl'

    xsl_path = os.path.join(my_path, xsl_filename)

    input_filename = yest_str + ".asAllRaw.xml"

    input_path = storage_dir + "oai/" + input_filename

    # input_path = "/Users/dwh2128/Documents/ACFA/OAI_local/20200426/20200426.asAllRaw.xml"  # test

    output_path = storage_dir + "test"  # test

    print(output_path)
    # output_path = os.path.join(my_path, 'output/fa_lists')  # test

    params = "output_dir=" + output_path

    x = util.saxon_process(saxon_path, input_path, xsl_path, None, params)
    print(x)


if __name__ == "__main__":
    main()
