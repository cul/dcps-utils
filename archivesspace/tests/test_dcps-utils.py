# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings'.
import dcps_utils as util
import json
import os

# import logging

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)

some_data = [
    ["a", "b", "c"],
    [1, 2, 3],
    [4, 5, 6],
    [0, 2, 10],
    [1, 22, 33],
    [7, 2, 100],
]

some_data2 = [
    [1, "b", "c"],
    [2, 2, 3],
    [4, 5, 6],
    [3, 2, 10],
    [22, 22, 33],
    [7, 2, 100],
]


def test_saxon_process():
    # Test XSLT transform using Saxon
    in_file = os.path.join(MY_PATH, "../xslt/OAI_SAMPLE.asClean.xml")
    xsl_file = os.path.join(MY_PATH, "../xslt/extract-bibids.xsl")
    params = "filename=" + in_file
    x = util.saxon_process(in_file, xsl_file, None, theParams=params)
    assert "BibID: 4078817" in x


def test_jing_process():
    # Test return of schema errors in invalid file
    in_file = os.path.join(MY_PATH, "../xslt/EAD_SAMPLE.xml")
    schema_file = os.path.join(MY_PATH, "../schemas/cul_as_ead.rng")
    x = util.jing_process(in_file, schema_file)
    assert 'error: value of attribute "normal" is invalid;' in x


def test_get_status_200():
    x = util.get_status("https://findingaids.library.columbia.edu/")
    assert x == 200


def test_get_status_404():
    x = util.get_status("https://www.example.com/notapage")
    assert x == 404


def test_diff():
    x = util.diff(["a", "b", "c", 1, 2, 3], [3, 4, 5, "c", "d"])
    assert x == ["a", "b", 1, 2]


def test_dedupe_array():
    # Reduce array to only rows with unique values in col 1.
    x = util.dedupe_array(some_data, 1)
    assert len(x) == 4


def test_trim_array():
    x = util.trim_array(some_data, [1, 2])
    assert x[2] == [4]


def test_sort_array():
    x = util.sort_array(some_data2)
    assert x[2][0] == 3


def test_pickle_it():
    pickle_path = os.path.join(MY_PATH, "output/some_data.pickle")
    if os.path.exists(pickle_path):
        os.remove(pickle_path)
    util.pickle_it(some_data, pickle_path)
    x = util.unpickle_it(pickle_path)
    assert x[0] == some_data[0]


def test_find_config():
    assert "config.ini" in util.find_config()
