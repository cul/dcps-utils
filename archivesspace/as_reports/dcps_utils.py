import subprocess
from configparser import ConfigParser
import os

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

    if server == "Dev":
        oaiURL = config["DEV"]["baseOAIURL"]
    elif server == "Test":
        oaiURL = config["TEST"]["baseOAIURL"]
    else:
        oaiURL = config["PROD"]["baseOAIURL"]

    cmd = (
        "/usr/bin/python "
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
    # This will always work but is kludgy.
    subprocess.call(cmd, shell=True)


# TODO: Test different subprocess params...
def oai_harvest2(
    out_path,
    output_type="oai_marc",
    server="Prod",
    date_params="",
    harvester_path=os.path.join(my_path, "pyoaiharvester/pyoaiharvest.py"),
):

    if server == "Dev":
        oaiURL = config["DEV"]["baseOAIURL"]
    elif server == "Test":
        oaiURL = config["TEST"]["baseOAIURL"]
    else:
        oaiURL = config["PROD"]["baseOAIURL"]

    cmd = (
        "/usr/bin/python "
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




def saxon_process(saxonPath, inFile, transformFile, outFile, theParams=" "):
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
        + " > "
        + outFile
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
        return "SAXON ERROR: " + str(result[1].decode("utf-8"))
    else:
        return result[0].decode("utf-8")


if __name__ == "__main__":
    main()
