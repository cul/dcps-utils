# Checks that Voyager integration is working. Runs as part of pytest exec.
import as_daily_check_clio as clio


def test_clio_check():
    assert clio.check_clio() == True
