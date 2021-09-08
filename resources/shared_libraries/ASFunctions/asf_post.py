import json
import requests
import csv

# import sys
import os

# from configparser import ConfigParser
from .asf_main import (
    ASAuthenticate,
    getIt,
    postIt,
    valid_repos,
)


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


#################
### FUNCTIONS ###
#################


###################################
# Functions to post data          #
###################################


def postArchivalObject(repo, asid, record):
    """POST archival object

    Args:
        repo (int): repo id
        asid (int): asid of archival object
        record (str): JSON object (archival object)

    Returns:
        str: JSON response from POST
    """
    headers = ASAuthenticate()
    endpoint = "repositories/" + str(repo) + "/archival_objects/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postAgent(asid, record, agent_type="people"):
    """POST agent

    Args:
        asid (int): asid of agent
        record (str): JSON agent record
        agent_type (str, optional): Options: people, families, corporate_entities. Defaults to "people".

    Returns:
        str: JSON response from POST
    """
    # types: people, families, corporate_entities
    headers = ASAuthenticate()
    endpoint = "agents/" + agent_type + "/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postDigitalObject(repo, asid, record):
    """POST digital object

    Args:
        repo (int): repo id
        asid (int): asid of digital object
        record (str): JSON object (digital object)

    Returns:
        str: JSON response from POST
    """
    headers = ASAuthenticate()
    endpoint = "repositories/" + str(repo) + "/digital_objects/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postEnumeration(asid, record):
    """POST enumeration

    .. todo::
       This perhaps does not work?

    Args:
        asid (int): ID of enumeration
        record (str): JSON object (record)

    Returns:
        str: JSON response

    """
    # TODO: This perhaps does not work?
    headers = ASAuthenticate()
    endpoint = "config/enumerations/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postEnumerationValue(asid, record):
    headers = ASAuthenticate()
    endpoint = "config/enumeration_values/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postResource(repo, asid, record):
    """POST resource

    Args:
        repo (int): repo id
        asid (int): asid of resource
        record (str): JSON object (resource)

    Returns:
        str: JSON response from POST
    """
    headers = ASAuthenticate()
    endpoint = "repositories/" + str(repo) + "/resources/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postSubject(asid, record):
    """POST subject

    Args:
        asid (int): repo id
        record (str): JSON object (subject)

    Returns:
        str: JSON response
    """
    headers = ASAuthenticate()
    endpoint = "subjects/" + str(asid)
    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def postTopContainer(repo, asid, record):
    """POST top container

    Args:
        repo (int): repo id
        asid (int): asid of top container
        record (str): JSON object (top container)

    Returns:
        str: JSON response from POST
    """
    headers = ASAuthenticate()
    endpoint = "repositories/" + str(repo) + "/top_containers/" + str(asid)

    post = postIt(endpoint, headers, record)
    post = json.dumps(post)
    return post


def suppressEnumerationValue(asid, mode="suppress"):
    """Suppress/unsuppres an enumeration value. Options 'unsuppress', 'suppress'

    Args:
        asid (int): ID of enumeration value
        mode (str, optional): Options: "suppress", "unsuppress". Defaults to "suppress".

    Returns:
        str: JSON response from POST
    """
    # Set mode to 'unsuppress' to do so, otherwise suppress
    suppress_flag = "suppressed=true" if mode == "suppress" else "suppressed=false"
    headers = ASAuthenticate()
    endpoint = (
        "/config/enumeration_values/" + str(asid) + "/suppressed?" + suppress_flag
    )
    # TODO: add postIt method without record data? Test this.
    post = postIt(endpoint, headers, "")
    post = requests.post(baseURL + endpoint, headers=headers).json()
    post = json.dumps(post)
    return post


def unpublishArchivalObject(repo, asid):
    """Unpublish archival object

    .. todo:: Move this function to an "update" set as it uses both GET and POST.

    Args:
        repo (int): repo id
        asid (int): id of archival object

    Returns:
        str: JSON response
    """
    from .asf_get import getArchivalObject

    x = getArchivalObject(repo, asid)
    y = json.loads(x)
    y["publish"] = False
    z = json.dumps(y)
    return postArchivalObject(repo, asid, z)
