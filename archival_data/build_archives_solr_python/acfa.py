# acfa.py
import subprocess
import re


def run_bash(cmd, errorPrefix=''):
    print(cmd)
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    #DEBUG
    # print("0: " + fix_cr(str(result[0].decode('utf-8'))) )
    # print("1: " + fix_cr(str(result[1].decode('utf-8'))) )
    if result[1]:  # error
        # print(errorPrefix + 'ERROR: ' + str(result[1].decode('utf-8')))
        # return errorPrefix + 'ERROR: ' + str(result[1].decode('utf-8'))
        raise Exception(errorPrefix + 'ERROR: ' +
                        fix_cr(str(result[1].decode('utf-8'))))
    print(result[0].decode('utf-8')) # test
    return result[0].decode('utf-8')


# def run_saxon(saxonPath, inFile, transformFile, outFile, theParams=' '):
#     cmd = 'java -jar ' + saxonPath + ' ' + inFile + ' ' + transformFile + ' ' + \
#         theParams + ' ' + '--suppressXsltNamespaceCheck:on' + ' > ' + outFile
#     return run_bash(cmd, 'SAXON ')


def run_saxon(saxonPath, inFile, transformFile, outFile, theParams=' '):
    # TODO: Test error parsing.
    # Process an XSLT transformation. Use None for outFile to send to stdout.
    outStr = " > " + outFile if outFile else " "
    cmd = (
        "java -jar "
        + saxonPath
        + " "
        + inFile
        + " "
        + transformFile
        + " "
        + theParams
        + " "
        + "--suppressXsltNamespaceCheck:on"
        + outStr
    )
    # print(cmd)
    p = subprocess.Popen(
        [cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    result = p.communicate()
    if result[1]:
        if "error" in str(result[1].decode("utf-8")).lower():
            # error
            raise Exception("SAXON ERROR: " + str(result[1].decode("utf-8")))
        elif "does not exist" in str(result[1].decode("utf-8")).lower():
            # error
            raise Exception("SAXON ERROR: " + str(result[1].decode("utf-8")))
        elif "java.io" in str(result[1].decode("utf-8")).lower():
            # error
            raise Exception("SAXON ERROR: " + str(result[1].decode("utf-8")))
        elif "permission denied" in str(result[1].decode("utf-8")).lower():
            # error
            raise Exception("SAXON ERROR: " + str(result[1].decode("utf-8")))
        else:
            # non-error output
            return "SAXON MESSAGE: " + str(result[1].decode("utf-8"))
    else:
        return result[0].decode("utf-8")


# def run_post(solr_xml_path, solr_update_url):
#     cmd = 'curl -i -X POST {0} -H "Content-Type: text/xml" --data-binary "@{1}"'.format(
#         solr_update_url, solr_xml_path)
#     return run_bash(cmd, 'SOLR ')

def run_post(solr_xml_path, solr_update_url):
    cmd = 'curl -i -X POST {0} -H "Content-Type: text/xml" --data-binary "@{1}"'.format(solr_update_url, solr_xml_path)
    print(cmd)
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    if '200' not in str(result[0].decode('utf-8')) and '201' not in str(result[0].decode('utf-8')):
        raise Exception('SOLR ERROR: Reponse other than 200/201!')
    elif 'Error' in str(result[1].decode('utf-8')):
        raise Exception('SOLR ERROR: ' +
                        fix_cr(str(result[1].decode('utf-8'))))
    print(fix_cr(str(result[1].decode('utf-8'))))
    return result[0].decode('utf-8')


def sanitize_xml(in_path, out_path):
    # strip out some bad bytes that will foul up parsing.
    with open(in_path, "r") as f:
        content = f.read()
    repl = re.subn(r"[\x01-\x08\x0b\x0c\x0e-\x1f]",
                   "?", content, flags=re.DOTALL)
    with open(out_path, "w+") as f:
        f.write(repl[0])
    if repl[1] > 0:
        return "WARNING: Replaced " + str(repl[1]) + " illegal characters in " + in_path

def fix_cr(_str):
    return re.sub(r"\x0D", "\n", _str, flags=re.DOTALL)
