# import subprocess
import requests
import os
# import re
# import datetime
from sheetFeeder import dataSheet
import dcps_utils as util
import csv


def main():

    # test_url = 'https://dx.doi.org/10.7916/d8-nfd2-zc36'
    # test_url = 'http://www.columbia.edu/cu/lweb/indiv/rbml/index.html'
    # test_url = 'http://localhost:8081/repositories/2/resources/1356'

    # x = get_response(test_url)
    # print(x)
    # quit()

    my_name = __file__
    script_name = os.path.basename(my_name)

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    # the_sheet = dataSheet(
    #     '1sjpjLt_I54h9l-ABwueYdN6xVAm01S6rKZB3BgMQv3k', 'test!A:Z')

    the_output_sheet = dataSheet(
        '1sjpjLt_I54h9l-ABwueYdN6xVAm01S6rKZB3BgMQv3k', 'output!A:Z')

    # the_sheet_data = the_sheet.getData()
    # the_heads = the_sheet_data.pop(0)

    # aCSV = '/Users/dwh2128/Documents/ACFA/TEST/ACFA-252-audit-links/output_test2.txt'
    # aCSV = os.path.join(my_path, 'output/acfa-252-carnegie-urls.txt')
    aCSV = os.path.join(my_path, 'output/acfa-252-all-urls.txt')

    the_data = []

    the_csv = open(aCSV)
    for row in csv.reader(the_csv, delimiter='|'):
        the_data.append(row)
    the_csv.close()

    the_heads = the_data.pop(0)
    the_heads += ['STATUS', 'REDIRECT_LOCATION', 'REDIRECT_STATUS']
    the_new_data = [the_heads]

    for a_row in the_data:
        print(a_row)
        response = get_response(a_row[2])
        if response['status'] != 200:
            new_row = a_row
            while len(new_row) < 5:
                new_row.append("")
            new_row.append(response['status'])
            if 'location' in response:
                redirect_response = get_response(response['location'])
                new_row += [response['location'], redirect_response['status']]

            print(new_row)
            the_new_data.append(new_row)

    the_output_sheet.clear()
    the_output_sheet.appendData(the_new_data)


def get_response(url):
    try:
        x = requests.head(url)
        status = x.status_code

        if status in [301, 302]:
            location = x.headers['Location']
        else:
            location = ""
            # print(x.headers['Location'])
        # print(x.headers)

    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as e:
        status = "ERROR: " + str(e)
        location = ""

    response = {'status': status}
    if location:
        response['location'] = location
    return response


if __name__ == "__main__":
    main()
