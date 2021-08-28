import json
import requests
import csv
import sys
import os
from configparser import ConfigParser


#
# Compilation of ArchivesSpace API functions.
# See README for config.ini setup.

# Usage: from another python script, add
#   import ASFunctions as asf
#
# Then call functions like
#   asf.getResource(2,4277)
#
#


global baseURL
global user
global password
global session_token
global config


my_name = __file__

# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

config_path = os.path.join(my_path, "../config.ini")


try:
    # See if there is an initial session token in environment to use.
    session_token = os.environ["session"]
except:
    session_token = ""


# Set server to Prod as default. Override in parent script with
# ASFunctions.setServer('Test') or ASFunctions.setServer('Dev').
try:
    # Read default config values
    config = ConfigParser()
    config.read(config_path)

    baseURL = config["PROD"]["baseURL"]
    user = config["PROD"]["user"]
    password = config["PROD"]["password"]
    # List of used AS repo codes
    valid_repos = json.loads(config["REPOS"]["validRepos"])

    # Get proxy url if there is one.
    if "httpsProxy" in config["PROXIES"]:
        https_proxy = config["PROXIES"]["httpsProxy"]
    else:
        https_proxy = None
except Exception as e:
    print("Error: There was a problem reading the config.ini file." + str(e))
    sys.exit(1)


def main():
    # Test functions here.

    quit()


#######################################
# Authentication and global handlers  #
#######################################

# Returns session headers for next API call, either using existing session token or generating one.


def ASAuthenticate(user, baseURL, password):
    """Main authentication handler. Called by other functions.

    Args:
        user (str): username
        baseURL (str): Base API URL
        password (str): password

    Returns:
        dict: Headers with session token for use in API calls.
    """
    global session_token
    if session_token != "":
        # there is already a token in env
        headers = {
            "X-ArchivesSpace-Session": session_token,
            "Content_Type": "application/json",
        }
    else:
        # generate a new token and save to env
        try:
            # get auth response including session token from API
            if https_proxy:
                auth = requests.post(
                    baseURL + "/users/" + user + "/login?password=" + password,
                    proxies={"https": https_proxy},
                ).json()
                msg = "(Authenticated using proxy " + https_proxy + ")"
            else:
                auth = requests.post(
                    baseURL + "/users/" + user + "/login?password=" + password
                ).json()
                msg = "(Authenticated)"

            if "error" in auth:
                print("AUTHENTICATION ERROR: " + auth["error"])
                sys.exit(1)
            else:
                print(msg)
            session_token = auth["session"]
            os.environ["session"] = session_token
        except Exception as e:
            print("Error: There was a problem authenticating to the API!" + str(e))
            sys.exit(1)
        headers = {
            "X-ArchivesSpace-Session": session_token,
            "Content_Type": "application/json",
        }
    return headers


# Generic fn to do GET with or without proxy, as defined by config.
def getIt(uri_str, headers, params=None, output="json"):
    """Generic fn to do GET with or without proxy, as defined by config.
    For internal use only.

    Args:
        uri_str (str): URI
        headers (dict): Headers including session token from ASAuthenticate
        params (dict, optional): Additional GET parameters. Defaults to None.
        output (str, optional): Output type (json|text). Defaults to "json".

    Returns:
        str: JSON object.
    """
    if https_proxy:
        response = requests.get(
            uri_str, headers=headers, params=params, proxies={"https": https_proxy}
        )
    else:
        response = requests.get(uri_str, headers=headers, params=params)
    if output == "json":
        return response.json()
    elif output == "text":
        return response.text
    else:
        print("ERROR: Output type " + output + " not recognized!")


# Generic fn to do POST with or without proxy, as defined by config.


def postIt(uri_str, headers, data):
    """Generic fn to do POST with or without proxy, as defined by config.
    For internal use only.

    Args:
        uri_str (str): URL
        headers (dict): Headers including session token
        data (str): JSON object to post

    Returns:
        str: JSON response
    """
    if https_proxy:
        return requests.post(
            uri_str, headers=headers, data=data, proxies={"https": https_proxy}
        ).json()
    else:
        return requests.post(uri_str, headers=headers, data=data).json()


# Set server to 'Prod' (default) | 'Test' | 'Dev'
def setServer(server):
    """Set AS server for subsequent API calls ('Prod' (default) | 'Test' | 'Dev')

    Args:
        server (str): Server name
    """
    global baseURL
    global user
    global password
    global config
    global session_token
    session_token = ""  # start with fresh auth token
    if server == "Dev":
        baseURL = config["DEV"]["baseURL"]
        user = config["DEV"]["user"]
        password = config["DEV"]["password"]
    elif server == "Test":
        baseURL = config["TEST"]["baseURL"]
        user = config["TEST"]["user"]
        password = config["TEST"]["password"]
    else:
        baseURL = config["PROD"]["baseURL"]
        user = config["PROD"]["user"]
        password = config["PROD"]["password"]


if __name__ == "__main__":
    main()
