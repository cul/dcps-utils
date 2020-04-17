# Script to report various data to GSheet/dashboard.

import json
import ASFunctions as asf
from pprint import pprint
from sheetFeeder import dataSheet
from operator import itemgetter
from datetime import datetime, date, timedelta
import re
import os.path
import subprocess


def main():

    asf.setServer('Prod')  # AS instance: Prod | Dev | Test

    mode = 'Prod'  # Prod or Test

    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    now1 = datetime.now()
    start_time = str(now1)
    end_time = ''  # set later
    # today_str = str(date.today().strftime("%Y%m%d"))
    yest_str = str((date.today() - timedelta(days=1)).strftime("%Y%m%d"))

    ########################
    ### PROCESS OAI DATA ###
    ########################

    # Set path to Saxon processor
    saxon_path = os.path.join(my_path, "../../resources/saxon-9.8.0.12-he.jar")

    # XSLT file to generate report
    marc_xslt_file = os.path.join(my_path, 'marcDataExtract.xsl')

    if mode == 'Prod':
        # OAI XML file to use as source
        # source_dir='/cul/cul0/lito/libsys/voyager/prod/data/loads/AS_harvest'
        source_dir = '/cul/cul0/ldpd/archivesspace/oai'
        sheet_id = '198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY'
        oai_file = source_dir + '/' + yest_str + '.asRaw.xml'

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

    # Copy oai current data to oai_last sheet for diff
    the_old_data = the_sheets['oai'].getData()
    the_sheets['oai_last'].clear()
    the_sheets['oai_last'].appendData(the_old_data)
    # Process OAI MARC and output to CSV
    saxon_process(saxon_path, oai_file, marc_xslt_file, the_outpath)

    # clear data from "new" sheet
    the_sheets['oai'].clear()

    # Send result csv to Google Sheet.
    y = the_sheets['oai'].importCSV(the_outpath, delim='|')

    print(' ')

    ########################
    ### PROCESS UNPUBLISHED ###
    ########################

    print('Finding unpublished records...')

    the_repos = [2, 3, 4, 5]
    the_fields = ['id', 'title', 'identifier', 'create_time',
                  'system_mtime', 'last_modified_by', 'json']
    the_heads = ['REPO', 'REPO_ID', 'RESOURCE_ID', 'TITLE',
                 'BIBID', 'CREATE_TIME', 'SYSTEM_MTIME', 'LAST_MODIFIED_BY']

    unpubs_sheet = dataSheet(sheet_id, 'unpublished!A:Z')

    the_unpublished = []

    for r in the_repos:
        print('searching repo ' + str(r))

        x = asf.getUnpublished(r, filter='resources', fields=the_fields)
        # print(x)

        for a in x:
            row = [a[v] for v in the_fields]
            # print(row)
            my_json = json.loads(row.pop(6))
            try:
                call_no = my_json['user_defined']['string_1']
            except:
                call_no = ''
            # get the repo from the uri string.
            repo_id = int(str(row[0].split('/')[-3]).rstrip())
            # get the asid from the uri string.
            asid = int(str(row[0].split('/')[-1]).rstrip())
            row.pop(0)
            row.insert(0, asid), row.insert(0, repo_id)
            if 'UA' in call_no:
                repo = 'nnc-ua'
            else:
                repo = get_repo(repo_id)
            row.insert(0, repo)
            the_unpublished.append(row)
        print('Repo ' + str(r) + ': ' + str(len(x)))

    print('Total unpublished: ' + str(len(the_unpublished)))

    unpubs_sheet.clear()
    unpubs_sheet.appendData([the_heads])
    unpubs_sheet.appendData(the_unpublished)

    ########################
    ### GET NEWLY CREATED ###
    ########################

    data_data = [
        {'range': 'resource-changes!A:Z', 'filter': 'resources'}, {
            'range': 'accession-changes!A:Z', 'filter': 'accessions'}
    ]

    for d in data_data:

        print('processing ' + d['filter'])

        the_delta_sheet = dataSheet(sheet_id, d['range'])

        the_date = yest_str
        # the_date = '2019-08-27'
        the_repos = [2, 3, 4, 5]
        the_fields = ['id', 'title', 'identifier', 'create_time',
                      'system_mtime', 'last_modified_by', 'publish']

        the_heads = ['repo', 'asid', 'title', 'identifier',
                     'create_time', 'system_mtime', 'last_modified_by', 'publish']

        the_modifieds = []

        for r in the_repos:

            print('searching repo ' + str(r))

            x = asf.getByDate(r, the_date, date_type='ctime',
                              comparator='equal', filter=d['filter'], fields=the_fields)
            for a in x:
                row = [a[v] for v in the_fields]
                # print(row)
                # get the repo from the uri string.
                repo = str(row[0].split('/')[-3]).rstrip()
                # get the asid from the uri string.
                asid = str(row[0].split('/')[-1]).rstrip()
                row.pop(0)
                row.insert(0, asid), row.insert(0, repo)

                the_modifieds.append(row)
                # print(list(a.values()))
                # the_modifieds.append(list(a.values()))
            print('Repo ' + str(r) + ': ' + str(len(x)))

        print('Total ' + d['filter'] + ': ' + str(len(the_modifieds)))
        # the_sheet.clear()

        # the_sheet.appendData([the_fields])
        the_delta_sheet.appendData(the_modifieds)

    ########################
    ### FINISH UP ###
    ########################

    # Generate log string.
    now2 = datetime.now()
    end_time = str(now2)
    my_duration = str(now2 - now1)

    the_log = 'Data imported by ' + my_name + '. Start: ' + start_time + \
        '. Finished: ' + end_time + ' (duration: ' + my_duration + ').'

    the_sheets['log'].appendData([[the_log]])

    print(' ')

    print(the_log)

    print(' ')

    print('Script done. Updated data is available at ' + the_sheets['oai'].url)


def get_repo(repo_id):
    # Map repo codes
    if repo_id == 2:
        repo = 'nnc-rb'
    elif repo_id == 3:
        repo = 'nnc-a'
    elif repo_id == 4:
        repo = 'nnc-ea'
    elif repo_id == 5:
        repo = 'nnc-ut'
    else:
        repo = '-'
    return repo


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
    # Not used but could be useful!
    # Return list of x - y (everything in x that is not in y). Reverse order to get inverse diff.
    second = set(second)
    return [item for item in first if item not in second]


if __name__ == '__main__':
    main()
