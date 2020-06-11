import ASFunctions as asf
import json
from pprint import pprint
from sheetFeeder import dataSheet
import dcps_utils as util
import os.path
import csv
import datetime


asf.setServer('Prod')

my_name = __file__


# This makes sure the script can be run from any working directory and still find related files.
my_path = os.path.dirname(__file__)

# sheet_id = '1gUx1cPS8POLxqRblYIs1vlpr7yDGOyHmAJqpl6nMo4k'
sheet_id = '1e43qKYvqGQFOMxA70U59yPKPs18y-k3ohRNdU-qrTH0'  # test

# list_sheet = dataSheet(sheet_id, 'report!A:Z')
list_sheet = dataSheet(sheet_id, 'test!A:Z')  # test

the_data = list_sheet.getData()

the_heads = the_data.pop(0)

today = datetime.date.today().strftime("%Y-%m-%d")

# This is the location to add.
container_location = {
    "status": "current",
    "jsonmodel_type": "container_location",
    "start_date": today,
    "ref": "/locations/2",
}

col_position = 12  # which column to look at for Y/N

for a_row in the_data:
    if len(a_row) > col_position:
        if a_row[col_position] == "Y":
            print("Yes")
            bibid = a_row[0]
            tc = a_row[2]
            repo = tc.split('/')[2]
            asid = tc.split('/')[4]
            ils_holding_id = a_row[8]
            ils_item_id = a_row[9]
            barcode = a_row[10]

            print(bibid)
            print(tc)
            print(repo)
            print(asid)
            print(ils_holding_id)
            print(ils_item_id)
            print(barcode)

            x = asf.getTopContainer(repo, asid)

            # convert to dict and add in the new data
            y = json.loads(x)

            y['ils_holding_id'] = ils_holding_id
            y['ils_item_id'] = ils_item_id
            y['barcode'] = barcode
            # y['container_locations'].append(container_location)
            y['container_locations'] = [container_location]

            # convert back to json for post
            z = json.dumps(y)

            post = asf.postTopContainer(repo, asid, z)
            print(post)

    else:
        print("Skipping " + str(a_row[0]) + "...")
