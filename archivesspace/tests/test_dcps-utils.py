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


def test_saxon_process2():
    in_file = os.path.join(MY_PATH, '../xslt/OAI_SAMPLE.asClean.xml')
    xsl_file = os.path.join(MY_PATH, '../xslt/extract-bibids.xsl')
    params = 'filename=' + in_file
    x = util.saxon_process2(in_file, xsl_file, None, theParams=params)
    assert 'BibID: 4078817' in x


def test_get_status_200():
    x = util.get_status('https://findingaids.library.columbia.edu/')
    assert x == 200


def test_get_status_404():
    x = util.get_status('https://www.example.com/notapage')
    assert x == 404


def test_diff():
    x = util.diff(['a', 'b', 'c', 1, 2, 3], [3, 4, 5, 'c', 'd'])
    assert x == ['a', 'b', 1, 2]


def test_dedupe_array():
    # Reduce array to only rows with unique values in col 1.
    data = [['a', 'b', 'c'], [1, 2, 3], [4, 5, 6],
            [0, 2, 10], [1, 22, 33], [7, 2, 100]]
    x = util.dedupe_array(data, 1)
    assert len(x) == 4


def test_trim_array():
    data = [['a', 'b', 'c'], [1, 2, 3], [4, 5, 6],
            [0, 2, 10], [1, 22, 33], [7, 2, 100]]
    x = util.trim_array(data, [1, 2])
    assert x[2] == [4]
