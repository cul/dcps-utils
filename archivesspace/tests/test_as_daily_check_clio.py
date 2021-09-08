# Checks that Voyager integration is working. Runs as part of pytest exec.
import archivesspace.as_crons.as_daily_check_clio as clio
import datetime
import os


TODAY = datetime.date.today().strftime("%Y%m%d")
YESTERDAY = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
DAY_BEFORE_YESTERDAY = (datetime.date.today() - datetime.timedelta(days=1)).strftime(
    "%Y%m%d"
)

SOURCE_FOLDER = "/cul/cul0/ldpd/archivesspace/oai"


def test_clio_check():
    # the_date = TODAY if clio.is_after("20:01:01") else YESTERDAY
    #! Won't work to test in same day, as Voyager sync doesn't
    #! happen until next night. Needs to run on prev day files.
    # the_date = YESTERDAY
    the_date = DAY_BEFORE_YESTERDAY
    xml_path = os.path.join(SOURCE_FOLDER, the_date + ".asRaw.xml")

    assert clio.check_clio(the_date, xml_path) == True
