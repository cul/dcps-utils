# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings'.
import archivesspace.as_crons.generate_fa_lists as fa
import os
from datetime import date, timedelta


# import logging

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)


STORAGE_DIR = "/cul/cul0/ldpd/archivesspace/"
YEST_STR = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))
TEST_BIBID = 12471376  # Wright drawings in Avery


def test_extract_record_list():
    repo = "nnc-a"
    xsl_path = os.path.join(MY_PATH, "../xslt/generate_browse_list2.xsl")
    input_path = os.path.join(MY_PATH, STORAGE_DIR, "oai/" + YEST_STR + ".asAllRaw.xml")
    x = fa.extract_record_list(repo, input_path, xsl_path)
    y = [i["bibid"] for i in x if i["bibid"] == TEST_BIBID]
    assert TEST_BIBID in y
    assert len(y) > 20
