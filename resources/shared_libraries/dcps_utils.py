import subprocess
from configparser import ConfigParser
import os
import pickle
import requests
import copy
import time
import re

my_path = os.path.dirname(__file__)
# harvester_path = os.path.join(my_path, "pyoaiharvester/pyoaiharvest.py")
config_path = os.path.join(my_path, "config.ini")
config = ConfigParser()
config.read(config_path)


def oai_harvest(
    out_path,
    output_type="oai_marc",
    server="Prod",
    date_params="",
    harvester_path=os.path.join(my_path, "pyoaiharvester/pyoaiharvest.py"),
):
    """Harvest OAI-PMH records from ArchivesSpace and save to file. See https://github.com/vphill/pyoaiharvester

    Args:
        out_path (str): Local file path
        output_type (str, optional): Output type. Defaults to "oai_marc".
        server (str, optional): Prod, Test, or Dev. Defaults to "Prod".
        date_params (str, optional): From/until date parameters, using format -f yyyy-mm-dd -u format: yyyy-mm-dd. Defaults to "".
        harvester_path (str, optional): File path to pyoaiharvest.py. Defaults to os.path.join(my_path, "pyoaiharvester/pyoaiharvest.py").

    Returns:
        str: stdout result
    """
    if server == "Dev":
        oaiURL = config["DEV"]["baseOAIURL"]
    elif server == "Test":
        oaiURL = config["TEST"]["baseOAIURL"]
    else:
        oaiURL = config["PROD"]["baseOAIURL"]

    cmd = (
        "python "
        + harvester_path
        + " -l "
        + oaiURL
        + " -m "
        + output_type
        + " -s collection"
        + " -o "
        + out_path
        + " "
        + date_params
    )
    print(cmd)
    p = subprocess.Popen(
        [cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    result = p.communicate()
    if result[1]:  # error
        return "PYOAIHARVEST ERROR: " + str(result[1].decode("utf-8"))
    else:
        return result[0].decode("utf-8")


def saxon_process(
    inFile,
    transformFile,
    outFile,
    theParams=" ",
    saxonPath=config["FILES"]["saxonPath"],
):
    """Process an XSLT transformation using Saxon.

    Args:
        inFile (str): Path to input XML
        transformFile (str): Path to XSLT
        outFile (str): Path to output file. Use None to send to stdout.
        theParams (str, optional): Additional parameters, as defined by stylesheet. Defaults to " ".
        saxonPath (str, optional): Path to Saxon. Defaults to config["FILES"]["saxonPath"].

    Raises:
        Exception: "SAXON ERROR: <error message>

    Returns:
        str: Result stdout
    """
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
    if not result[1]:
        return result[0].decode("utf-8")

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


def jing_process(
    filePath, schemaPath, compact=False, jingPath=config["FILES"]["jingPath"]
):
    """Process an xml file against a schema (rng or schematron) using Jing.

    Args:
        filePath (str): Path to input file
        schemaPath (str): Path to schema file
        compact (bool, optional): Use "compact" RelaxNG schema format. Defaults to False.
        jingPath (str, optional): Path to Jing. Defaults to config["FILES"]["jingPath"].

    Returns:
        str: Result stdout
    """
    # Process an xml file against a schema (rng or schematron) using Jing.
    # Tested with jing-20091111.
    # https://code.google.com/archive/p/jing-trang/downloads
    # -d flag (undocumented!) = include diagnostics in output.
    # -c flag is for compact schema format.
    flags = " -cd " if compact is True else " -d "
    cmd = "java -jar " + jingPath + flags + schemaPath + " " + filePath
    # print(cmd)
    p = subprocess.Popen(
        [cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    result = p.communicate()
    if result[1]:  # error
        return "SAXON ERROR: " + str(result[1].decode("utf-8"))
    else:
        return result[0].decode("utf-8")


def rsync_process(fromPath, toPath, options="", keyPath=config["FILES"]["keyPath"]):
    """Rsync files in a given directory

    Args:
        fromPath (str): Path to directory to sync from
        toPath (str): Path to directory to sync to
        options (str, optional): Rsync additional option flags, e.g., "--exclude '\*.zip'". Defaults to False.
        keyPath (str, optional): Path to ssh key. Defaults to config["FILES"]["keyPath"].

    Returns:
        str: Result stdout
    """
    if keyPath:
        cmd = (
            '/usr/bin/rsync -zarvhe "ssh -i '
            + keyPath
            + '" '
            + options
            + " "
            + fromPath
            + " "
            + toPath
        )
    else:
        cmd = "/usr/bin/rsync -zavh " + options + " " + fromPath + " " + toPath

    print("Running command: " + cmd + " ...")
    print(" ")

    result = subprocess.Popen(
        [cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    ).communicate()

    if result[1]:  # error
        return "RSYNC ERROR: " + str(result[1].decode("utf-8"))
    else:
        return result[0].decode("utf-8")


def pickle_it(obj, path):
    """Save object as pickle file

    Args:
        obj (dict, list): Python object (e.g., dict) to pickle
        path (str): Path to output file
    """
    print("Saving pickle to " + str(path) + "...")
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def unpickle_it(path):
    """Unpickle a pickle file

    Args:
        path (str): Path to pickle to unpickle

    Returns:
        dict or list: The unpickled objects
    """
    print("Unpickling from " + str(path) + "...")
    with open(path, "rb") as f:
        output = pickle.load(f)
    return output


def get_clio_marc(bibid):
    """Retrieve MARC data from CLIO via http

    Args:
        bibid (str): BIBID

    Raises:
        Exception: get_clio_marc request error

    Returns:
        binary: MARC21 data
    """
    url = "https://clio.columbia.edu/catalog/" + str(bibid) + ".marc"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as err:
        raise Exception("*** get_clio_marc request error: " + str(err))
    else:
        # If the response was successful, no exception will be raised
        return response.content


def get_status(url):
    """Get http status code for URL

    Args:
        url (str): URL

    Returns:
        int: Status code
    """
    response = requests.get(url)
    return response.status_code


def check_clio_status(bibid):
    """Check that a BIBID has a publicly available CLIO record. If using in bulk, add sleep of .5 sec or more to avoid "too many requests" error.

    Args:
        bibid (str): BIBID

    Returns:
        int: HTTP status code
    """
    # If using in bulk, add sleep of .5 sec or more to
    # avoid "too many requests" error
    return get_status("https://clio.columbia.edu/catalog/" + str(bibid))


def diff(first, second):
    """Diff two lists. Return list of x - y (everything in x that is not in y). Reverse order to get inverse diff.

    Args:
        first (list): List1
        second (list): List2

    Returns:
        List: The list of items in List1 that are not in List2.
    """
    second = set(second)
    return [item for item in first if item not in second]


def dedupe_array(data, col):
    """For a 2D array (list of lists), remove rows that have duplicate data in a given column. Provide column on which to match dupes (starts with 0).

    Args:
        data (list): 2-dimensional array
        col (int): Column to match for duplicates (starts with 0)

    Returns:
        list: Result array with duplicates removed.
    """
    new_data = []
    for row in data:
        if row[col] not in [r[col] for r in new_data]:
            new_data.append(row)
    return new_data


def trim_array(data, indices):
    """Trim columns from array. Provide column indexes as list to remove (starts with 0). Leaves original array intact (by deep copying)

    Args:
        data (list): 2-dimensional array (list of lists)
        indices (list): List of integer column indexes (starting with 0)

    Returns:
        list: New list with columns trimmed
    """
    new_data = copy.deepcopy(data)
    for row in new_data:
        for i in sorted(indices, reverse=True):
            del row[i]
    return new_data


def sort_array(data, match_key=0, ignore_heads=False):
    """Sort an array based on given column (1st one by default)

    Args:
        data (list): 2-dimensional array (list of lists)
        match_key (int, optional): Column to sort on. Defaults to 0.
        ignore_heads (bool, optional): Treat row 0 as heads and ignore. Defaults to False.

    Returns:
        list: New sorted list
    """
    data_sorted = copy.deepcopy(data)
    if ignore_heads:
        heads = data_sorted.pop(0)
    data_sorted.sort(key=lambda x: x[match_key])
    if ignore_heads:
        data_sorted.insert(0, heads)
    return data_sorted


def file_cleanup(_dir, _days):
    """Remove files from a directory that are of a certain age.

    Args:
        _dir (str): Path to directory
        _days (int): Number of days beyond which old files should be deleted
    """
    # Remove files from a directory that are of a certain age.
    now = time.time()
    old = now - int(_days) * 24 * 60 * 60
    # print(old)
    for f in os.listdir(_dir):
        path = os.path.join(_dir, f)
        if os.path.isfile(path):
            stat = os.stat(path)
            # print("")
            # print(stat.st_mtime)
            if stat.st_mtime < old:
                print("removing: ", path)
                os.remove(path)


#! TEST  ###


def run_bash(cmd, errorPrefix=""):
    """Run a command in bash

    Args:
        cmd (str): Command
        errorPrefix (str, optional): Prefix to apply to any error outputs, e.g., for logging, raising exceptions. Defaults to "".

    Raises:
        Exception: Error output (if any), with prefix applied

    Returns:
        str: Result stdout
    """
    # print(cmd)
    p = subprocess.Popen(
        [cmd],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    result = p.communicate()
    # DEBUG
    # print("0: " + fix_cr(str(result[0].decode('utf-8'))) )
    # print("1: " + fix_cr(str(result[1].decode('utf-8'))) )
    if result[1]:  # error
        # print(errorPrefix + 'ERROR: ' + str(result[1].decode('utf-8')))
        # return errorPrefix + 'ERROR: ' + str(result[1].decode('utf-8'))
        raise Exception(
            errorPrefix + "ERROR: " + fix_cr(str(result[1].decode("utf-8")))
        )
    # print(result[0].decode('utf-8'))  # test
    return result[0].decode("utf-8")


def fix_cr(_str):
    """Replace all \x0D with \n in string

    Args:
        _str (str): Input string

    Returns:
        str: Output string
    """
    return re.sub(r"\x0D", "\n", _str, flags=re.DOTALL)
