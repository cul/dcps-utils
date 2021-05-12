# Script to extract repo information from Solr XML files, to aid finding aids app to construct canonical URLs based on bibid.


import subprocess
import os


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    solr_output_folder = '/cul/cul0/ldpd/archival_data/solr'
    destination_folder = '/cul/cul0/ldpd/archival_data/bib_ids'  # test
    destination_folder = '/cul/cul0/ldpd/archival_data/test/bib_ids'  # test
    xslt_file = 'solr_repo_extract.xsl'

    saxon_path = os.path.join(my_path, "../../resources/saxon-9.8.0.12-he.jar")
    xslt_path = os.path.join(my_path, xslt_file)
    out_path = os.path.join(destination_folder, 'valid_fa_bib_ids.yml')
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


if __name__ == '__main__':
    main()
