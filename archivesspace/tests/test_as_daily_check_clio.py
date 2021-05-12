# Checks that Voyager integration is working. Runs as part of pytest exec.
import archivesspace.as_crons.as_daily_check_clio as clio
import datetime
import os


TODAY = datetime.date.today().strftime("%Y%m%d")
YESTERDAY = (datetime.date.today() -
             datetime.timedelta(days=1)).strftime("%Y%m%d")

SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/oai"


def test_clio_check():
    the_date = TODAY if clio.is_after("20:01:01") else YESTERDAY
    xml_path = os.path.join(SOURCE_FOLDER, the_date + ".asRaw.xml")

    assert clio.check_clio(the_date, xml_path) == True
