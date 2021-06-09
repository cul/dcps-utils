# Script to extract repo information from Solr XML files, to aid finding aids app to construct canonical URLs based on bibid.

import subprocess
import os
from shutil import copyfile
import datetime


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    MY_PATH = os.path.dirname(__file__)

    TODAY = datetime.date.today().strftime("%Y%m%d")
    YESTERDAY = (datetime.date.today() -
                 datetime.timedelta(days=1)).strftime("%Y%m%d")

    solr_output_folder = '/cul/cul0/ldpd/archival_data/solr'
    destination_folder = '/cul/cul0/ldpd/archival_data/bib_ids'
    # destination_folder = '/cul/cul0/ldpd/archival_data/test/bib_ids'  # test
    out_path = os.path.join(destination_folder, 'valid_fa_bib_ids.yml')

    make_dated_backup(out_path, TODAY)  # make a backup with date.
    xslt_file = 'solr_repo_extract.xsl'
    saxon_path = os.path.join(MY_PATH, "../../resources/saxon-9.8.0.12-he.jar")
    xslt_path = os.path.join(MY_PATH, xslt_file)
    the_params = 'source_dir=' + solr_output_folder

    print('Processing files in ' + solr_output_folder)
    response = saxon_process(
        saxon_path, xslt_path, xslt_path, out_path, theParams=the_params)

    print(response)


def saxon_process(saxonPath, inFile, transformFile, outFile, theParams=' '):
    cmd = 'java -jar ' + saxonPath + ' ' + inFile + ' ' + transformFile + ' ' + \
        theParams + ' ' + '--suppressXsltNamespaceCheck:on' + ' > ' + outFile
    print(cmd)
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    if result[1]:  # error
        return 'SAXON ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')


def make_dated_backup(filepath, date):
    # make a copy of file in same directory with date prepended.
    dir = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    newpath = os.path.join(dir, str(date) + '_' + filename)
    return copyfile(filepath, newpath)


if __name__ == '__main__':
    main()
