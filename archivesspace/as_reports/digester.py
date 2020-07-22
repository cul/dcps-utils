from sheetFeeder import dataSheet
from datetime import datetime

digest_sheet = '190p6gnhpakdYD72Eb1PLicdVlAtAxjQ7D_8oee7Tk1U'
digest_range = 'Sheet1!A:Z'

digest_sheet = dataSheet(digest_sheet, digest_range)


def main():

    # TEST
    # date = str(datetime.today().isoformat())
    # print(date)

    # quit()

    digest_clear()
    x = post_digest('test_script', 'here is some info')


def digest_clear(sheet=digest_sheet):
    post = sheet.clear()
    return post


def post_digest(script_name, log, sheet=digest_sheet):
    date = str(datetime.today())
    data = [[script_name, date, log]]
    post = sheet.appendData(data)
    return post


if __name__ == "__main__":
    main()
