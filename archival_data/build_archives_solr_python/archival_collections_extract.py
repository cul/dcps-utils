# Script to transform MARC XML (output from archiverun.sh, see ACFA-118) to SOLR XML for posting to Archives Portal index.

import acfa
import os
import re


def main():
    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    marc_data_folder = '/cul/cul0/ldpd/archival_data/marc/archives_portal'
    solr_output_folder = '/cul/cul0/ldpd/archival_data/solr'
    # saxon_path = os.environ['HOME'] + '/lib/saxon-9he.jar'
    saxon_path = '/opt/dcps/resources/saxon-9.8.0.12-he.jar'
    xslt_path = os.path.join(my_path, 'marc2solr.xsl')

    the_repos = [
        {'data_file': 'AV.xml', 'clean_file': 'AV_clean.xml', 'repo_id': 'nnc-a'},
        {'data_file': 'EA.xml', 'clean_file': 'EA_clean.xml', 'repo_id': 'nnc-ea'},
        {'data_file': 'HS.xml', 'clean_file': 'HS_clean.xml', 'repo_id': 'nnc-m'},
        {'data_file': 'CCOH.xml', 'clean_file': 'CCOH_clean.xml', 'repo_id': 'nnc-ccoh'},
        {'data_file': 'RB.xml', 'clean_file': 'RB_clean.xml', 'repo_id': 'nnc-rb'},
        {'data_file': 'UA.xml', 'clean_file': 'UA_clean.xml', 'repo_id': 'nnc-ua'},
        {'data_file': 'UT.xml', 'clean_file': 'UT_clean.xml', 'repo_id': 'nnc-ut'}
    ]

    transform_paths = []
    error_pattern = re.compile("^SAXON ERROR")
    for r in the_repos:
        raw_file_path = marc_data_folder + '/' + r['data_file']
        clean_file_path = marc_data_folder + '/' + r['clean_file']
        repo_id = r['repo_id']
        out_path = solr_output_folder + '/' + repo_id + '_solr' + '.xml'
        the_params = 'repo=' + repo_id

        print('Processing ' + r['data_file'] + '...')

        # strip out bad characters if any. See ACFA-270.
        acfa.sanitize_xml(raw_file_path, clean_file_path)

        # transform to solr xml
        response = acfa.run_saxon(
            saxon_path, clean_file_path, xslt_path, out_path, theParams=the_params)

        print(response)
        if not error_pattern.match(response):
            transform_paths.append(out_path)
    return transform_paths


if __name__ == '__main__':
    main()
