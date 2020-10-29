# Script to retrieve Oral History MARC XML via fetchOralHistoryRecords and transform to to SOLR XML for posting to OH Portal index.

import acfa
import os


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    # extract_script_path = '/cul/cul0/ldpd/ccoh/fetchOralHistoryRecords'
    extract_script_path = os.path.join(
        my_path, 'fetchOralHistoryRecords')  # TEST
    # marc_output_path = '/cul/cul0/ldpd/archival_data/marc/oral_history_portal/ohac_marc.xml'
    marc_output_path = '../output/ohac_marc.xml'  # TEST
    # solr_output_path = '/cul/cul0/ldpd/archival_data/solr/ohac_solr.xml'
    solr_output_path = '../output/ohac_solr.xml'  # TEST
    # saxon_path = os.environ['HOME'] + '/lib/saxon-9he.jar'
    saxon_path = '../../resources/saxon-9.8.0.12-he.jar'  # TEST
    xslt_path = os.path.join(my_path, 'oral2solr.xsl')

    # remove existing file so fetchOralHistoryRecords won't fail.
    if os.path.exists(marc_output_path):
        print("Removing old file at " + marc_output_path)
        os.remove(marc_output_path)

    the_shell_command = extract_script_path + ' --output ' + marc_output_path

    print('Extracting OHAC MARC data from Voyager...')

    print(acfa.run_bash(the_shell_command))

    # Do regex to remove some illegal characters. See ACFA-270.
    acfa.sanitize_xml(marc_output_path, marc_output_path)

    print('Transforming MARC to SOLR XML...')

    response = acfa.run_saxon(
        saxon_path, marc_output_path, xslt_path, solr_output_path)
    print(response)
    if response.find('SAXON ERROR') > -1:
        return []
    else:
        return [solr_output_path]


if __name__ == '__main__':
    main()
