# Script to run nightly against the "allRaw" OAI xml file from the previous day.

import json
from pprint import pprint
from sheetFeeder import dataSheet  # test
from operator import itemgetter
from datetime import datetime, date, timedelta
import re
import os.path
import subprocess


def main():

    # set Prod | Dev | Test
    # target_server = 'Prod'  # Prod | Dev | Test
    # asf.setServer(target_server)

    mode = 'Prod'  # Prod or Test

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    # Set path to Saxon processor
    saxon_path = os.path.join(my_path, "../resources/saxon-9.8.0.12-he.jar")

    # XSLT file to generate report
    xslt_file = os.path.join(my_path, '../xslt/marcDataExtract.xsl')

    now1 = datetime.now()
    start_time = str(now1)
    end_time = ''  # set later
    # today_str = str(date.today().strftime("%Y%m%d"))
    yest_str = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))

    # print('Script ' + my_name + ' begun at ' + start_time + '. ')

    # the_data_sheet_new = dataSheet('198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY','oai!A:Z')
    # the_data_sheet_old = dataSheet('198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY','oai_last!A:Z')

    # the_diff_sheet = dataSheet('198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY','diff!A:Z')

    if mode == 'Prod':
        # OAI XML file to use as source
        source_dir = '/cul/cul0/lito/libsys/voyager/prod/data/loads/AS_harvest'
        sheet_id = '198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY'
        oai_file = source_dir + '/' + yest_str + '.asAllRaw.xml'

    else:  # TEST
        yest_str = "20190915"
        # OAI XML file to use as source
        source_dir = '/Users/dwh2128/Documents/ACFA/exist-local/backups/cached_eads/cached_eads_20190912'  # local test
        sheet_id = '1YzM1dinagfoTUirAoA2hHBfnhSM1PsPt8TkwTT9KlgQ'
        oai_file = yest_str + '.asAllRaw.xml'

    the_sheets = {'oai': dataSheet(sheet_id, 'oai!A:Z'),
                  'oai_last': dataSheet(sheet_id, 'oai_last!A:Z'),
                  'log': dataSheet(sheet_id, 'log!A:Z')
                  }

    the_outpath = os.path.join(
        my_path, 'output/' + yest_str + '.marc_reporter_out.xml')

    print(' ')

    # Capture the list of bibids, for use in doing a diff with new data to see what has been added or subtracted.

    # the_old_data = the_data_sheet.getData()

    # the_old_data_cols = the_data_sheet.getDataColumns()

    # the_old_ids = the_old_data_cols[0]
    # the_old_falinks = the_old_data_cols[7]

    the_old_data = the_sheets['oai'].getData()

    the_sheets['oai_last'].clear()

    the_sheets['oai_last'].appendData(the_old_data)

    # Process EADs and output to CSV
    saxon_process(saxon_path, oai_file, xslt_file, the_outpath)

    # clear data from "new" sheet
    the_sheets['oai'].clear()

    # Send result csv to Google Sheet.
    y = the_sheets['oai'].importCSV(the_outpath, delim='|')

    # the_new_data_cols = the_data_sheet.getDataColumns()

    # Capture the new list of bibids to compare to old list.
    # the_new_ids = the_new_data_cols[0]

    # Capture new list of fa links
    # the_new_falinks = the_new_data_cols[7]

    # the_adds = diff(the_new_ids,the_old_ids)
    # the_subtracts = diff(the_old_ids,the_new_ids)

    # Generate data to post for additions/subtractions
    # the_diff_data = []
    # for a in the_adds:
    #     the_diff_data.append([a,'added',yest_str,mode])
    # for s in the_subtracts:
    #     the_diff_data.append([s,'deleted',yest_str,mode])

    # head row
    # the_diff_data.insert(0, ['bibid','delta_type','delta_date'])

    # Post the diff data to the "diff" tab of report.
    # the_diff_sheet.clear()
    # the_diff_sheet.appendData(the_diff_data)

    print(' ')

    now2 = datetime.now()
    end_time = str(now2)
    my_duration = str(now2 - now1)

    the_log = 'Data imported from ' + oai_file + ' by ' + my_name + '. Start: ' + \
        start_time + '. Finished: ' + end_time + \
        ' (duration: ' + my_duration + ').'

    the_sheets['log'].appendData([[the_log]])

    print(' ')

    print(the_log)

    print(' ')

    print('Script done. Updated data is available at ' + the_sheets['oai'].url)


def saxon_process(saxonPath, inFile, transformFile, outFile, theParams=' '):
    cmd = 'java -jar ' + saxonPath + ' ' + inFile + ' ' + transformFile + ' ' + \
        theParams + ' ' + '--suppressXsltNamespaceCheck:on' + ' > ' + outFile
    print(cmd)
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    if result[1]:  # error
        return 'SAXON ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


if __name__ == '__main__':
    main()
