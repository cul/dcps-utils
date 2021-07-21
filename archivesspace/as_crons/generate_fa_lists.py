# Script to generate html snippets of lists of published finding aids.
# Run daily on cron. See ACFA-213.
# Depends on yaml file of bibids:repos extracted from the ArchivesPortal Solr
# index, to determine which AS collections are public.

import dcps_utils as util
import os
from datetime import datetime, date, timedelta
import yaml
from lxml import etree


def main():
    MY_NAME = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    MY_PATH = os.path.dirname(__file__)
    yest_str = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))

    # storage_dir = "../output/"  # test
    storage_dir = "/cul/cul0/ldpd/archivesspace/"

    # Location of yaml file output from solr_extract_repos.
    # Used to restrict output to only collections that are in Solr.
    # yaml_path = os.path.join(MY_PATH, storage_dir, "valid_fa_bib_ids.yml") # test
    yaml_path = "/cul/cul0/ldpd/archival_data/bib_ids/valid_fa_bib_ids.yml"

    # Use the OAI file from previous day as source to generate lists.
    input_path = os.path.join(MY_PATH, storage_dir, "oai/" + yest_str + ".asAllRaw.xml")

    # XSLT for transformation. Accepts a path in param in which to save the html snippet files.
    xsl_path = os.path.join(MY_PATH, "../xslt/generate_browse_list2.xsl")

    # The location to save output documents.
    # output_dir = os.path.join(MY_PATH, storage_dir + "fa_lists")
    output_dir = os.path.join(MY_PATH, storage_dir + "fa_lists")

    the_repos = ["nnc-a", "nnc-ea", "nnc-rb", "nnc-ua", "nnc-ut", "nnc-ccoh"]

    for r in the_repos:
        print(r)
        x = extract_record_list(r, input_path, xsl_path)
        y = filter_fa_list(x, yaml_path)
        z = create_fa_list(r, output_dir, y)
        print(z)


def extract_record_list(repo, oai_path, xsl_path, delim1="|", delim2="¶"):

    params = [
        ("repo", repo),
        ("delim1", delim1),
        ("delim2", delim2),
    ]

    param_string = parameterize(params)

    x = util.saxon_process(oai_path, xsl_path, None, theParams=param_string)

    return [
        {"bibid": r.split(delim1)[0], "title": r.split(delim1)[1]}
        for r in x.split(delim2)
    ]


def filter_fa_list(data, yaml_path):
    # take output of extract_record_list and filter based on Solr yaml file.
    with open(yaml_path, "r") as file:
        bib_list = yaml.load(file, Loader=yaml.FullLoader).keys()

    filtered_results = []
    for r in data:
        if int(r["bibid"]) not in bib_list:
            print("Warning: " + r["bibid"] + " not in Solr index!")
        else:
            filtered_results.append(r)
    return filtered_results


def parameterize(params):
    # Take a list of tuples (key/value) and construct a string to pass to Saxon
    return " ".join(i[0] + "='" + i[1] + "'" for i in params)


def create_fa_list(repo, output_dir, data, file_suffix="_fa_list.html"):
    # Generate and write an html snippet for fa list.
    output_path = os.path.join(output_dir, repo + file_suffix)
    root = etree.Element("ul")
    for r in data:
        item = etree.SubElement(root, "li")
        link = etree.SubElement(item, "a")
        link.attrib["href"] = "/ead/" + repo + "/ldpd_" + r["bibid"]
        link.text = r["title"]

    tree = etree.ElementTree(root)

    with open(output_path, "wb") as f:
        f.write(etree.tostring(tree, pretty_print=True))

    return "File written to " + output_path


if __name__ == "__main__":
    main()
