# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings'.
import digester
from sheetFeeder import dataSheet
import os
import datetime
import dateutil.parser


# import logging

MY_NAME = __file__

# This makes sure the script can be run from any working directory and still find related files.
MY_PATH = os.path.dirname(__file__)


FIXTURE_SHEET = dataSheet("1PLtSL1NHQ_PooSd2LkEDTHZMmhmrxPv4cv8STpmhknk", "fixture!A:Z")
FIXTURE_DATA = FIXTURE_SHEET.getData()
TEST_DATE = dateutil.parser.parse("2021-09-1")


def test_prune_data():
    l1 = len(FIXTURE_DATA)
    l2 = len(digester.prune_data(FIXTURE_DATA, 1, TEST_DATE))
    assert l2 < l1 and l2 == 37, "Length of pruned log should be 37."


def test_get_digest():
    new_digest = digester.get_digest(FIXTURE_SHEET)
    assert len(new_digest) == 2, "Digest should have two entries."


def test_date_is_recent():
    assert not digester.date_is_recent(
        TEST_DATE
    ), "Test date should not be considered recent (not within 24 hours of current datetime)"
