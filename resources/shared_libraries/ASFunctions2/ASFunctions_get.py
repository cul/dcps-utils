import json
import requests
import csv

# import sys
import os

from ASFunctions2.ASFunctions_main import (
    ASAuthenticate,
    getIt,
    postIt,
    baseURL,
    password,
    user,
    valid_repos,
    https_proxy,
    session_token,
    config_path,
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


# General function to get response from a provided endpoint string (must start with slash).
def getResponse(endpoint):
    """General function to get response from a provided endpoint string (must start with slash).

    Args:
        endpoint (str): API enpoint with args/params

    Returns:
        str: JSON response
    """
    headers = ASAuthenticate(user, baseURL, password)
    output = getIt(baseURL + endpoint, headers=headers)
    output = json.dumps(output)
    return output


#####################################
# Functions to get single objects   #
#####################################


def getArchivalObject(repo, asid):
    # supply repo and id
    """GET an archival object

    Args:
        repo (int): Repository code
        asid (int): ASID

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/archival_objects/" + str(asid)
    output = getIt(baseURL + endpoint, headers=headers)
    output = json.dumps(output)
    return output


def getArchivalObjectByRef(repo, ref):
    """GET archival object by ref_id, e.g., bed5f26c0673086345e624f9bbf1d1c5

    Args:
        repo (int): Repo code
        ref (str): AO ref id

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    params = {"ref_id[]": ref}
    endpoint = "/repositories/" + str(repo) + "/find_by_id/archival_objects"
    lookup = getIt(baseURL + endpoint, headers=headers, params=params)
    archival_object_uri = lookup["archival_objects"][0]["ref"]
    asid = archival_object_uri.split("/")[-1]
    return getArchivalObject(repo, asid)


def getCollectionManagement(repo, asid):
    """GET collection mangement by repo/asid

    Args:
        repo (int): repo id
        asid (int): asid

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/collection_management/" + str(asid)
    output = getIt(baseURL + endpoint, headers=headers)
    output = json.dumps(output)
    return output


def getEnumeration(asid):
    """GET an enumeration

    Args:
        asid (int): ID of enumeration

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/config/enumerations/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getEnumerationValue(asid):
    """GET enumeration value

    Args:
        asid (int): ID of enumeration

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/config/enumeration_values/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getResource(repo, asid):
    """GET resource by repo/asid

    Args:
        repo (int): repo id
        asid (int): asid

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/resources/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getResourceByID(bibid, repos=valid_repos):
    """Find resource across all valid repos using field 'identifier'=<bibid>.

    Args:
        bibid (int): BIBID
        repos (list, optional): List of valid repo codes. Defaults to valid_repos.

    Returns:
        str: JSON object of found resource
    """
    # Find resource across all valid repos using field 'identifier'=<bibid>.
    for r in repos:
        res = getResourceByRepoID(r, bibid)
        if res:
            return res


def getResourceByRepoID(repo, bibid):
    # Find and return resource based on repo and field 'identifier'=<bibid>.
    # Intended for use by getResourceByID.
    aquery = {
        "query": {
            "op": "AND",
            "subqueries": [
                {
                    "field": "primary_type",
                    "value": "resource",
                    "comparator": "equals",
                    "jsonmodel_type": "field_query",
                },
                {
                    "field": "identifier",
                    "value": str(bibid),
                    "comparator": "equals",
                    "jsonmodel_type": "field_query",
                },
            ],
            "jsonmodel_type": "boolean_query",
        },
        "jsonmodel_type": "advanced_query",
    }
    res = getSearchResults(repo, json.dumps(aquery))
    if len(res) == 1:
        return json.dumps(res[0])


def getDigitalObject(repo, asid):
    """GET digital object

    Args:
        repo (int): repo id
        asid (int): asid

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/digital_objects/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getDigitalObjectByRef(repo, ref):
    """GET digital object by AS ref id

    Args:
        repo (int): repo id
        ref (str): digital object ref id

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    params = {"resolve[]": "digital_objects", "digital_object_id[]": ref}
    endpoint = "/repositories/" + str(repo) + "/find_by_id/digital_objects"
    output = getIt(baseURL + endpoint, headers=headers, params=params)
    output = json.dumps(output)
    return output


def getDigitalObjectFromParent(repo, ref):
    # use an aspace id string like '59ad1b96a7786e6ab3e2a9aa2223dfcf', as found in EAD export of a parent archival object, to identify the digital object within and extract it.
    x = getArchivalObjectByRef(repo, ref)
    the_parent = json.loads(x)
    the_dao_refs = [
        inst["digital_object"]
        for inst in the_parent["instances"]
        if "digital_object" in inst
    ]

    results = []
    for dao_ref in the_dao_refs:
        uri = dao_ref["ref"]
        asid = str(uri.split("/")[-1])
        the_dao = getDigitalObject(repo, asid)
        results.append(the_dao)
    return results[0]  # is there ever more than one dao?


def getBibID(repo, asid):
    # return BibID from resource
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/resources/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    try:
        userDef = output["user_defined"]
        bibID = userDef["integer_1"]
    except:
        bibID = ""
    return bibID


def getAgent(asid, agent_type="people"):
    # types: people, families, corporate_entities
    """GET agent

    Args:
        asid (int): agent asid
        agent_type (str, optional): available types: people, families, corporate_entities. Defaults to "people".

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//agents/" + agent_type + "/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getAccession(repo, asid):
    """GET accession

    Args:
        repo (int): repo id
        asid (int): asid

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/accessions/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getSchema():
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//schemas"
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


def getEAD(repo, asid):
    # Returns EAD XML (not JSON)
    # https://archivesspace.github.io/archivesspace/api/#get-repositories-repo_id-resource_descriptions-id-xml
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = (
        "/repositories/"
        + str(repo)
        + "/resource_descriptions/"
        + str(asid)
        + ".xml"
        + "?include_unpublished=true&include_daos=true"
    )
    # optional parameters can be appended to the end of the above url - e.g. ?include_unpublished=true&include_daos=true&numbered_cs=true&print_pdf=true&ead3=true
    # output = requests.get(baseURL + endpoint, headers=headers).text
    output = getIt(baseURL + endpoint, headers=headers, output="text")
    return output


def lookupByBibID(aBibID, aCSV):
    # Lookup repo and ASID against lookup table csv.
    # Format of csv should be REPO,ASID,BIBID.
    lookupTable = open(aCSV)
    for row in csv.reader(lookupTable):
        if str(aBibID) in row[2]:
            return [row[0], row[1]]
    lookupTable.close()


def lookupBibID(repo, asid, aCSV):
    # Lookup repo and ASID against lookup table csv.
    # Format of csv should be REPO,ASID,BIBID.
    lookupTable = open(aCSV)
    for row in csv.reader(lookupTable):
        if str(repo) in row[0] and str(asid) in row[1]:
            return row[2]
    lookupTable.close()


def getResourceByBibID(aBibID, aCSV):
    myInfo = lookupByBibID(aBibID, aCSV)
    output = getResource(myInfo[0], myInfo[1])
    return output


def getAssessment(repo, asid):
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/assessments/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    # output = json.dumps(output)
    return output


def getSubject(id):
    """GET subject

    Args:
        id (int): asid

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/subjects/" + str(id)
    output = getIt(baseURL + endpoint, headers)
    # output = json.dumps(output)
    return output


def getTopContainer(repo, asid):
    """GET top container

    Args:
        repo (int): repo id
        asid (int): asid

    Returns:
        str: JSON object
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "/repositories/" + str(repo) + "/top_containers/" + str(asid)
    output = getIt(baseURL + endpoint, headers)
    output = json.dumps(output)
    return output


#####################################
# Functions to get multiple objects #
#####################################


def getAccessions(repo):
    """GET all accessions of a repo.

    Args:
        repo (int): repo id

    Returns:
        str: JSON list of accessions
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//repositories/" + str(repo) + "/accessions?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)

    records = []
    for id in ids:
        endpoint = "//repositories/" + str(repo) + "/accessions/" + str(id)
        output = getIt(baseURL + endpoint, headers)
        records.append(output)
        # print(output)
    output = json.dumps(records)
    return output


def getAgents(agent_type="people"):
    """GET all agents, filtered by type

    Args:
        agent_type (str, optional): Options: people, families, corporate_entities. Defaults to "people".

    Returns:
        list: List of agent records
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//agents/" + agent_type + "?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)
    # iterate over each returned ID, grabbing the json object
    records = []
    for id in ids:
        endpoint = "//agents/people/" + str(id)
        output = getIt(baseURL + endpoint, headers)
        records.append(output)
        # print(output)
    # output = json.dump(records)
    return records


def getArchivalObjectChildren(repo, asid):
    """GET a list of asids of children of an archival object.

    Args:
        repo (int): repo id
        asid (int): asid of archival object

    Returns:
        list: List of archival objects
    """
    # Get a list of asids of children of an archival object.
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = (
        "/repositories/" + str(repo) + "/archival_objects/" + str(asid) + "/children"
    )
    response = getIt(baseURL + endpoint, headers)
    return [x["uri"].split("/")[-1] for x in response]


def getAssessments(repo):
    """GET all assessments for a repo

    Args:
        repo (int): repo id

    Returns:
        str: JSON list of assessments
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//repositories/" + str(repo) + "/assessments?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)
    # iterate over each returned assessment, grabbing the json object
    records = []
    for id in ids:
        endpoint = "//repositories/" + str(repo) + "/assessments/" + str(id)
        output = getIt(baseURL + endpoint, headers)
        records.append(output)
        # print(output)
    output = json.dumps(records)
    return output


def getByDate(
    repo,
    date,
    date_type="ctime",
    comparator="equal",
    filter=None,
    fields=["id", "create_time", "title"],
):
    # Returns records with create_time <, =, or > than given date.
    # OPTIONAL FIELDS:
    #   comparators: equal (default), greater_than, lesser_than (not 'less_than'!)
    #   filters: None (default), archival_objects, resources, accessions,
    #      collection_managment, top_containers
    #   fields: Can be any field at top level of returned json object;
    #      these will form the output dict of each returned record.
    #   date_type: ctime or mtime (date created or date modified)

    # Select ctime or mtime based on param
    date_field = "create_time" if date_type == "ctime" else "system_mtime"
    aqparams = (
        '{"query":{"field":"'
        + date_field
        + '","value":"'
        + date
        + '","comparator":"'
        + comparator
        + '","jsonmodel_type":"date_field_query"},"jsonmodel_type":"advanced_query"}'
    )

    records = getSearchResults(repo, aqparams)

    # Filtering based on record type (archival_objects, resources, etc.)
    if filter == None:
        records_out = records
    else:
        records_out = [rec for rec in records if filter in rec["id"]]

    print("Number of matching records = " + str(len(records_out)))

    # Compile a dictionary for each record, based on which fields are requested (see defaults in def).
    output = []
    for r in records_out:
        rec_dict = {}
        for f in fields:
            # If field is not in a record (e.g., 'publish' is not in all types) the value will be empty.
            if f in r:
                rec_dict[f] = r[f]
            else:
                rec_dict[f] = ""
        output.append(rec_dict)

    return output


def getResources(repo):
    """GET all resources for a repo.

    Args:
        repo (int): repo id

    Returns:
        str: JSON list of resources
    """
    # https://archivesspace.github.io/archivesspace/api/#get-repositories-repo_id-resources-id
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//repositories/" + str(repo) + "/resources?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)

    records = []
    for id in ids:
        endpoint = "//repositories/" + str(repo) + "/resources/" + str(id)
        output = getIt(baseURL + endpoint, headers)
        records.append(output)
        # print(output)
    output = json.dumps(records)
    return output


def getResourceIDs(repo):
    """GET list of resource IDs for a repo, not the resources themselves.

    Args:
        repo (int): repo id

    Returns:
        str: JSON list of ids
    """
    # Return only the list of IDs, not the resources themselves
    # https://archivesspace.github.io/archivesspace/api/#get-repositories-repo_id-resources
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//repositories/" + str(repo) + "/resources?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)
    return ids


def getSubjects():
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//subjects?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)
    records = []
    for id in ids:
        endpoint = "//subjects/" + str(id)
        output = getIt(baseURL + endpoint, headers)
        records.append(output)
    return records


def getSearchResults(repo, query_params):
    """General function to process an advanced query and return unfiltered results. Intended to be called by other functions where the query string may be built by user input and the results parsed, e.g, getByCreateDate.
    Supply repo id and advanced query string of the form:

    x = getSearchResults(2, '{"query":{"field":"create_time", "value":"2019-08-13","comparator":"equal", "jsonmodel_type":"date_field_query"}, "jsonmodel_type":"advanced_query"}')

    See http://lyralists.lyrasis.org/pipermail/archivesspace_users_group/2015-May/001654.html for advanced query info.

    Args:
        repo (int): repo id
        query_params (str): parameters as string

    Returns:
        list: List or results found
    """

    records = []

    page_size = 100  # default
    pageno = 1  # default
    headers = ASAuthenticate(user, baseURL, password)

    endpoint = (
        "//repositories/"
        + str(repo)
        + "/search?page="
        + str(pageno)
        + "&page_size="
        + str(page_size)
        + "&aq="
        + query_params
    )
    response_init = getIt(baseURL + endpoint, headers)

    hit_count = response_init["total_hits"]
    # Check to see if hits exceed default page_size; if so, increase page_size to match hits and do API call again.

    print("Number of search hits: " + str(hit_count))

    if hit_count > page_size:

        # Check to see if count exceeds page size limit (250); if so, need to iterate through pages.
        if hit_count < 250:
            page_size = hit_count + 1  # add one, just for fun
            endpoint = (
                "//repositories/"
                + str(repo)
                + "/search?page="
                + str(pageno)
                + "&page_size="
                + str(page_size)
                + "&aq="
                + query_params
            )
            response = getIt(baseURL + endpoint, headers)
            records = response["results"]

        else:
            response_list = []
            # Hit count >= 250; need to paginate!
            page_size = 250
            # use divmod to get number of pages needed
            dm = divmod(hit_count, page_size)
            page_cnt = dm[0] if dm[1] == 0 else dm[0] + 1

            # print('page_cnt=' + str(page_cnt))

            for i in range(page_cnt):
                pageno = i + 1
                print("Fetching page " + str(pageno) + " of " + str(page_cnt))
                # run for each page
                endpoint = (
                    "//repositories/"
                    + str(repo)
                    + "/search?page="
                    + str(pageno)
                    + "&page_size="
                    + str(page_size)
                    + "&aq="
                    + query_params
                )
                response = getIt(baseURL + endpoint, headers)
                records.extend(response["results"])

    else:
        response = response_init
        records = response["results"]

    return records


def getUnpublished(repo, filter=None, fields=["id", "create_time", "title"]):
    """Returns unpublished records for a given repo. Any list of top-level fields can be selected to return in output.

    Args:
        repo (int): repo id
        filter (str, optional): Filter results to parent_type. Defaults to None.
        fields (list, optional): List of fields to return. Defaults to ["id", "create_time", "title"].

    Returns:
        list: List of dicts of results containing fields requested.
    """
    # Returns unpublished records for a given repo. Any list of top-level fields can be selected to return in output.

    aqparams = '{"query":{"field":"publish","value":false,"jsonmodel_type":"boolean_field_query"},"jsonmodel_type":"advanced_query"}'
    records = getSearchResults(repo, aqparams)
    # Filtering based on record type (archival_objects, resources, etc.)
    if filter == None:
        records_out = records
    else:
        records_out = [rec for rec in records if filter in rec["id"]]
    print("Number of matching records = " + str(len(records_out)))
    # Compile a dictionary for each record, based on which fields are requested (see defaults in def).
    output = []
    for r in records_out:
        rec_dict = {}
        for f in fields:
            # If field is not in a record (e.g., 'publish' is not in all types) the value will be empty.
            if f in r:
                rec_dict[f] = r[f]
            else:
                rec_dict[f] = ""
        output.append(rec_dict)
    return output


def getCollectionManagements(
    repo, filter=None, fields=["id", "parent_id", "title", "system_mtime"]
):
    """Returns list of collection management records for a given repo. Filter by parent type, i.e., resource | accession (default all). Any arbitrary set of top-level fields can be returned.

    Args:
        repo (int): repo id
        filter (str, optional): Parent type to filter by (resource, accession). Defaults to None.
        fields (list, optional): List of fields to return for each result. Defaults to ["id", "parent_id", "title", "system_mtime"].

    Returns:
        list: List of dicts with fields specified for each result.
    """
    # Returns list of collection management records for a given repo. Filter by parent type, i.e., resource | accession (default all). Any arbitrary set of top-level fields can be returned.

    aqparams = '{"query":{"field":"primary_type", "value":"collection_management", "jsonmodel_type":"field_query"},"jsonmodel_type":"advanced_query"}'
    records = getSearchResults(repo, aqparams)
    # Filtering based on parent type (resource, accession)
    if filter == None:
        records_out = records
    else:
        records_out = [rec for rec in records if filter in rec["parent_type"]]
    print("Number of matching records = " + str(len(records_out)))
    # Compile a dictionary for each record, based on which fields are requested (see defaults in def).
    output = []
    for r in records_out:
        rec_dict = {}
        for f in fields:
            # If field is not in a record the value will be empty.
            if f in r:
                rec_dict[f] = r[f]
            else:
                rec_dict[f] = ""
        output.append(rec_dict)
    return output


def getUsers():
    """GET all users

    Returns:
        str: JSON list of users
    """
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = "//users?all_ids=true"
    ids = getIt(baseURL + endpoint, headers)
    records = []
    for id in ids:
        endpoint = "//users/" + str(id)
        output = getIt(baseURL + endpoint, headers)
        records.append(output)
        output = json.dumps(records)
        return output


def daosRecurse(repo, asid):
    """Recursive function; only use in call from find_daos()!

    Args:
        repo (int): repo id
        asid (int): asid
    """
    # Recursive function; only use in call from find_daos()!
    headers = ASAuthenticate(user, baseURL, password)
    endpoint = (
        "/repositories/" + str(repo) + "/archival_objects/" + str(asid) + "/children"
    )
    x = getIt(baseURL + endpoint, headers)

    # Look for daos as children of archival object
    for a_child in x:
        # Debug: print(a_child['uri'])
        the_dao_refs = [
            inst["digital_object"]["ref"]
            for inst in a_child["instances"]
            if "digital_object" in inst
        ]
        if len(the_dao_refs) > 0:
            the_id = the_dao_refs[0].split("/")[-1]
            # Debug: print('Found a dao: ' + str(the_id))
            the_daos.append(the_id)
    # Only process children recursively if there are no daos (i.e. we are not at the file level yet).
    if len(the_daos) == 0:
        # Debug: print('going down one level...')
        next_gen = [a_child["uri"].split("/")[-1] for a_child in x]
        for an_id in next_gen:
            daosRecurse(repo, an_id)


def findDigitalObjectDescendants(repo, asid):
    """For any archival object, return a list of DAOs that are associated with children or descendants. Note: calls a recursive function, can take some time for large trees.

    Args:
        repo (int): repo id
        asid (int): asid of archival object

    Returns:
        list: List of digital object descendants
    """
    # For any archival object, return a list of DAOs that are associated with children or descendants.
    # Note: calls a recursive function, can take some time for large trees.
    global the_daos
    the_daos = []
    daosRecurse(repo, asid)
    return the_daos


if __name__ == "__main__":
    main()
