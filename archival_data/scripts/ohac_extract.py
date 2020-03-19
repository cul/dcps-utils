# Script to retrieve Oral History MARC XML via fetchOralHistoryRecords and transform to to SOLR XML for posting to OH Portal index.

import subprocess
import os


def main():


    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)


    extract_script_path = '/cul/cul0/ldpd/ccoh/fetchOralHistoryRecords'
    marc_output_path = '/cul/cul0/ldpd/archival_data/marc/oral_history_portal/ohac_marc.xml'
    solr_output_path = '/cul/cul0/ldpd/archival_data/solr/ohac_solr.xml'
    saxon_path = os.path.join(my_path, "../../resources/saxon-9.8.0.12-he.jar")
    xslt_path = os.path.join(my_path, 'oral2solr.xsl')

    the_shell_command = extract_script_path + ' --output ' + marc_output_path

    print('Extracting OHAC MARC data from Voyager...')

    print(run_bash(the_shell_command))


    print('Transforming MARC to SOLR XML...')

    x = saxon_process(saxon_path, marc_output_path,xslt_path,solr_output_path)
    print(x)






def run_bash(cmd):
    result = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    print(cmd)
    # result = subprocess.check_output([cmd], shell=True)
    # return result
    if result[1]: # error
        return 'ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')


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
