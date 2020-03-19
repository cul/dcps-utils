# Script to transform MARC XML (output from archiverun.sh, see ACFA-118) to SOLR XML for posting to Archives Portal index.

import subprocess
import os


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)


    marc_data_folder = '/cul/cul0/ldpd/archival_data/marc/archives_portal'
    solr_output_folder = '/cul/cul0/ldpd/archival_data/solr'
    # marc_data_folder = '/Users/dwh2128/Documents/ACFA/TEST/SOLR\ MIGRATION/incoming' #test
    # solr_output_folder = '/Users/dwh2128/Documents/ACFA/TEST/SOLR\ MIGRATION/Output' #test


    saxon_path = os.path.join(my_path, "../../resources/saxon-9.8.0.12-he.jar")
    xslt_path = os.path.join(my_path, 'marc2solr.xsl')

    the_repos = [
        {'data_file':'AV.xml','repo_id':'nnc-a'},
        {'data_file':'EA.xml','repo_id':'nnc-ea'}, 
        {'data_file':'HS.xml','repo_id':'nnc-m'}, 
        # {'data_file':'OH.xml','repo_id':'nnc-oh'},
        {'data_file':'RB.xml','repo_id':'nnc-rb'},
        {'data_file':'UA.xml','repo_id':'nnc-ua'},
        {'data_file':'UT.xml','repo_id':'nnc-ut'}
        ]


    for r in the_repos:
        file_path = marc_data_folder + '/' + r['data_file']
        repo_id = r['repo_id']
        out_path = solr_output_folder + '/' + repo_id + '_solr' + '.xml'
        the_params = 'repo=' + repo_id

        print('Processing ' + r['data_file'] + '...')
        response = saxon_process(saxon_path,file_path,xslt_path,out_path,theParams=the_params )

        print(response)




def saxon_process(saxonPath, inFile, transformFile, outFile, theParams=' '):
    cmd = 'java -jar ' + saxonPath + ' ' + inFile  + ' ' + transformFile + ' ' + theParams + ' ' + '--suppressXsltNamespaceCheck:on' + ' > ' + outFile
    print(cmd)
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    if result[1]: # error
        return 'SAXON ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')




if __name__ == '__main__':
    main()
