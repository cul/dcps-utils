# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings --tb=short'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings --tb=short'.
import archivesspace.as_crons.generate_fa_lists as fa
import os
from datetime import date, timedelta


# import logging

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)


STORAGE_DIR = "/cul/cul0/ldpd/archivesspace/"
YAML_PATH = "/cul/cul0/ldpd/archival_data/bib_ids/valid_fa_bib_ids.yml"
YEST_STR = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))
TEST_BIBID = "12471376"  # Wright drawings in Avery
XSL_PATH = os.path.join(MY_PATH, "../xslt/generate_browse_list2.xsl")
OAI_PATH = os.path.join(MY_PATH, STORAGE_DIR, "oai/" + YEST_STR + ".asAllRaw.xml")


def test_extract_record_list():
    repo = "nnc-a"
    x = fa.extract_record_list(repo, OAI_PATH, XSL_PATH)
    y = [i["bibid"] for i in x if i["bibid"] == TEST_BIBID]
    assert TEST_BIBID in y
    assert len(x) > 20


def test_filter_results():
    repo = "nnc-ccoh"
    x = fa.extract_record_list(repo, OAI_PATH, XSL_PATH)
    x.append({"bibid": "9999999", "title": "TEST TITLE"})
    y = fa.filter_fa_list(x, YAML_PATH)
    z = [i["bibid"] for i in y]
    print(z)
    assert "9999999" not in y
