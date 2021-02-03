# Requires pytest. Checks basic connectivity and read functions from sample data sheet.
# Run all tests with 'pytest --disable-pytest-warnings'.
# If in virtual environment, use 'python -m pytest --disable-pytest-warnings'.
import as_reports.ASFunctions as asf
import json
# import logging


asf.setServer('Prod')

def test_get_resource():
    x = json.loads(asf.getResource(2, 5907))
    assert x['id_0'] == '4078601', "BIBID should be 4078601"

