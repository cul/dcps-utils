# Script to retrieve Oral History MARC XML via fetchOralHistoryRecords and transform to to SOLR XML for posting to OH Portal index.

import subprocess
import os
import re


def main():

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    extract_script_path = './fetchOralHistoryRecords2'
    marc_output_path = '../output/ohac_marc_test.xml'
    marc_output_clean_path = '../output/ohac_marc_test_clean.xml'
    solr_output_path = '../output/ohac_solr_test.xml'
    saxon_path = os.path.join(my_path, "../../resources/saxon-9.8.0.12-he.jar")
    xslt_path = os.path.join(my_path, 'oral2solr.xsl')

    if os.path.exists(marc_output_path):
        print("Removing old file at " + marc_output_path)
        os.remove(marc_output_path)

    the_shell_command = extract_script_path + ' --output ' + marc_output_path

    print('Extracting OHAC MARC data from Voyager...')

    print(run_bash(the_shell_command))

    print('Transforming MARC to SOLR XML...')

    # do regex to remove some illegal characters.
    sanitize_xml(marc_output_path, marc_output_clean_path)

    x = saxon_process(saxon_path, marc_output_clean_path,
                      xslt_path, solr_output_path)
    print(x)


def run_bash(cmd):
    result = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, shell=True).communicate()
    print(cmd)
    # result = subprocess.check_output([cmd], shell=True)
    # return result
    if result[1]:  # error
        return 'ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')


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


def sanitize_xml(in_path, out_path):
    # strip out some bad bytes that will foul up parsing.
    with open(in_path, "r") as f:
        content = f.read()
        # content_new = re.sub(
        #     "[\x01-\x08\x0b\x0c\x0e-\x1f]", r"", content, flags=re.MULTILINE
        # )
        repl = re.subn(r"[\x01-\x08\x0b\x0c\x0e-\x1f]",
                       r"?", content, flags=re.DOTALL)

        if repl[1] > 0:
            print("Warning: Replaced " +
                  str(repl[1]) + " illegal characters in " + in_path)

        with open(out_path, "w+") as f:
            f.write(repl[0])


if __name__ == '__main__':
    main()
