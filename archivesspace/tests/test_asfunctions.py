# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings'.
import ASFunctions as asf
import json

# import logging


def test_set_server():
    asf.setServer("Test")
    assert (
        asf.baseURL == "https://aspace-test.library.columbia.edu/api/"
    ), "baseURL for Test should be https://aspace-test.library.columbia.edu/api/"


def test_get_resource_prod():
    asf.setServer("Prod")
    assert (
        json.loads(asf.getResource(2, 5907))["id_0"] == "4078601"
        and asf.baseURL == "https://aspace.library.columbia.edu/api/"
    ), "Prod: BIBID for resource 2:5907 on Prod should be 4078601"


def test_get_resource_test():
    asf.setServer("Test")
    assert (
        json.loads(asf.getResource(2, 5907))["id_0"] == "4078601"
        and asf.baseURL == "https://aspace-test.library.columbia.edu/api/"
    ), "Test: BIBID for resource 2:5907 on Test should be 4078601"


def test_get_resource_dev():
    asf.setServer("Dev")
    assert (
        json.loads(asf.getResource(2, 5907))["id_0"] == "4078601"
        and asf.baseURL == "https://aspace-dev.library.columbia.edu/api/"
    ), "Dev: BIBID for resource 2:5907 should be 4078601"
