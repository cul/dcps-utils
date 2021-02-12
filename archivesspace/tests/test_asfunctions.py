# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings'.
import as_reports.ASFunctions as asf
import json
# import logging


asf.setServer('Prod')


def test_get_resource_prod():
    x = json.loads(asf.getResource(2, 5907))
    assert x['id_0'] == '4078601', "Prod: BIBID for resource 2:5907 should be 4078601"


asf.setServer('Test')


def test_get_resource_test():
    x = json.loads(asf.getResource(2, 5907))
    assert x['id_0'] == '4078601', "Test: BIBID for resource 2:5907 should be 4078601"


asf.setServer('Dev')


def test_get_resource_dev():
    x = json.loads(asf.getResource(2, 5907))
    assert x['id_0'] == '4078601', "Dev: BIBID for resource 2:5907 should be 4078601"
