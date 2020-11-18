import sys
import os
import acfa2 as acfa
import re
# module for reporting;
# TODO: reorganize into importable resources package.
sys.path.insert(1, '/opt/dcps/archivesspace/as_reports')
import digester

my_name = __file__
script_name = os.path.basename(my_name)
my_path = os.path.dirname(__file__)


def main():

    solr_index_envs = []
    if len(sys.argv) > 1:
        solr_index_envs = sys.argv[1].split(',')
    else:
        # Exit because there was no argument dev|test|prod.
        sys.exit("Error: No solr_index_env argument(s) provided!")
    solr_update_urls = ["http://ldpd-solr-" + solr_index_env +
                        "1.cul.columbia.edu:8983/solr/archives_portal/update" for solr_index_env in solr_index_envs]
    for solr_xml_path in archival_collections_extract():
        for solr_update_url in solr_update_urls:
            acfa.run_post(solr_xml_path, solr_update_url)
    for solr_xml_path in ohac_extract():
        for solr_update_url in solr_update_urls:
            acfa.run_post(solr_xml_path, solr_update_url)
    my_path = os.path.dirname(__file__)
    commit_xml_path = os.path.join(my_path, 'commit.xml')
    delete_xml_path = os.path.join(my_path, 'delete-delta.xml')
    for solr_update_url in solr_update_urls:
        # commit the document add/updates
        acfa.run_post(commit_xml_path, solr_update_url)
        # delete everything that wasn't added/updated in this job
        acfa.run_post(delete_xml_path, solr_update_url)
        # commit the deletes
        acfa.run_post(commit_xml_path, solr_update_url)


def archival_collections_extract():
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
    # error_pattern = re.compile("^SAXON ERROR")
    for r in the_repos:
        raw_file_path = marc_data_folder + '/' + r['data_file']
        clean_file_path = marc_data_folder + '/' + r['clean_file']
        repo_id = r['repo_id']
        out_path = solr_output_folder + '/' + repo_id + '_solr' + '.xml'
        the_params = 'repo=' + repo_id

        print('Processing ' + r['data_file'] + '...')

        # strip out bad characters if any. See ACFA-270.
        res = acfa.sanitize_xml(raw_file_path, clean_file_path)
        if res:
            print(res)
            digester.post_digest(script_name,res) # reporting

        # transform to solr xml
        response = acfa.run_saxon(
            saxon_path, clean_file_path, xslt_path, out_path, theParams=the_params)

        print(response)
        if "ERROR" not in response:
            transform_paths.append(out_path)
    return transform_paths


def ohac_extract():
    # extract_script_path = '/cul/cul0/ldpd/ccoh/fetchOralHistoryRecords'
    extract_script_path = os.path.join(my_path, './fetchOralHistoryRecords')
    marc_output_path = '/cul/cul0/ldpd/archival_data/marc/oral_history_portal/ohac_marc.xml'
    marc_output_clean_path = '/cul/cul0/ldpd/archival_data/marc/oral_history_portal/ohac_marc_clean.xml'
    solr_output_path = '/cul/cul0/ldpd/archival_data/solr/ohac_solr.xml'
    # saxon_path = os.environ['HOME'] + '/lib/saxon-9he.jar'
    saxon_path = '/opt/dcps/resources/saxon-9.8.0.12-he.jar'
    xslt_path = os.path.join(my_path, 'oral2solr.xsl')

    # remove existing file so fetchOralHistoryRecords won't fail.
    if os.path.exists(marc_output_path):
        print("Removing old file at " + marc_output_path)
        os.remove(marc_output_path)

    the_shell_command = extract_script_path + ' --output ' + marc_output_path

    print('Extracting OHAC MARC data from Voyager...')

    res = acfa.run_bash(the_shell_command)
    # print(res)
    digester.post_digest(script_name,res) # reporting

    # Do regex to remove some illegal characters. See ACFA-270.
    res = acfa.sanitize_xml(marc_output_path, marc_output_clean_path)
    if res:
        print(res)
        digester.post_digest(script_name,res) # reporting

    print('Transforming MARC to SOLR XML...')

    response = acfa.run_saxon(
        saxon_path, marc_output_clean_path, xslt_path, solr_output_path)
    print(response)
    if "ERROR" in response:
        return []
    else:
        return [solr_output_path]


if __name__ == '__main__':
    main()
