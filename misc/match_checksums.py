# Extract matches from a csv matching on checksums.

import csv
from sheetFeeder import dataSheet


# the_sheet = dataSheet(
#     '1ogPrdAFe1tpoGPxMXXtdrQjaGe1g_XG0OMdSaaxNZs8', 'digital-matches!A:Z')

sheet_id = '1ogPrdAFe1tpoGPxMXXtdrQjaGe1g_XG0OMdSaaxNZs8'

# checksum_sheet = dataSheet(sheet_id, 'ebooks_2011')


the_sheet = dataSheet(sheet_id, 'digital-matches2!A:Z')

# the_csv = '/Users/dwh2128/Documents/Cleanup_Project/fstore-subfolders/911-audio-pres.csv'
# the_checksum_list = '/Users/dwh2128/Documents/Cleanup_Project/fstore-subfolders/911-checksums.csv'
the_checksum_list = '/Users/dwh2128/Documents/Cleanup_Project/fstore-subfolders/ebooks_2011_checksums.csv'
the_csv = '/Users/dwh2128/Documents/Cleanup_Project/duplicates-non-ifp-filtered.csv'


the_sheet.clear()

with open(the_checksum_list) as f:
    the_checksums = [r[0] for r in csv.reader(f)]

the_matches = []
with open(the_csv) as f:
    for r in csv.reader(f):
        if r[0] in the_checksums and '/digital/' in r[1]:
            the_matches.append([r[0], r[1] + r[2]])


# print(the_checksums)

# print(the_matches)
print(len(the_matches))

the_sheet.appendData(the_matches)
