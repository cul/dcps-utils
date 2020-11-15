# acfa.py
import subprocess
import re


def run_bash(cmd, errorPrefix=''):
    print(cmd)
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    if result[1]:  # error
        return errorPrefix + 'ERROR: ' + str(result[1].decode('utf-8'))
        # raise Exception(errorPrefix + 'ERROR: ' +
        #                 str(result[1].decode('utf-8')))
    else:
        return result[0].decode('utf-8')


def run_saxon(saxonPath, inFile, transformFile, outFile, theParams=' '):
    cmd = 'java -jar ' + saxonPath + ' ' + inFile + ' ' + transformFile + ' ' + \
        theParams + ' ' + '--suppressXsltNamespaceCheck:on' + ' > ' + outFile
    return run_bash(cmd, 'SAXON ')


def run_post(solr_xml_path, solr_update_url):
    cmd = 'curl -i -X POST {0} -H "Content-Type: text/xml" --data-binary "@{1}"'.format(
        solr_update_url, solr_xml_path)
    return run_bash(cmd, 'SOLR ')


def sanitize_xml(in_path, out_path):
    # strip out some bad bytes that will foul up parsing.
    with open(in_path, "r") as f:
        content = f.read()
    repl = re.subn(r"[\x01-\x08\x0b\x0c\x0e-\x1f]",
                   r"?", content, flags=re.DOTALL)
    if repl[1] > 0:
        print("Warning: Replaced " +
              str(repl[1]) + " illegal characters in " + in_path)
    with open(out_path, "w+") as f:
        f.write(repl[0])
