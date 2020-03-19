# Script to query API for resources modified/created on a certain date


import os
import datetime
import ASFunctions as asf
from ASFunctions import getSearchResults
from sheetFeeder import dataSheet
from datetime import datetime, date, timedelta
# import re
import json
from pprint import pprint


def main():

    asf.setServer('Prod')

    # the_repos=[2,3,4,5]
    the_repos=[2]
    the_fields = ['id','title','identifier','create_time','system_mtime','last_modified_by','json']

    the_sheet=dataSheet('198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY','unpublished!A:Z')


    the_unpublished = []

    for r in the_repos:
        print('searching repo ' + str(r))
            
        x = getUnpublished(r,filter='resources',fields=the_fields)
        # print(x)

        for a in x:
            row = [ a[v] for v in the_fields ]
            my_json = json.loads(row.pop(6))
            try:
                call_no = my_json['user_defined']['string_1']
            except: 
                call_no = ''
            repo_id = int(str(row[0].split('/')[-3]).rstrip()) # get the repo from the uri string.
            asid = int(str(row[0].split('/')[-1]).rstrip()) # get the asid from the uri string.
            row.pop(0)
            row.insert(0,asid), row.insert(0,repo_id)
            if 'UA' in call_no:
                repo = 'nnc-ua'
            else:
                repo = get_repo(repo_id)
            row.insert(0,repo)
            the_unpublished.append(row)
            print(row)
        print('Repo ' + str(r) + ': ' + str(len(x)))

    print('Total unpublished: ' + str(len(the_unpublished)))

    # the_sheet.clear()
    # the_sheet.appendData([the_fields])
    # the_sheet.appendData(the_unpublished)


    quit()


def get_repo(repo_id):
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



def getUnpublished(repo,filter=None,fields=['id','create_time','title']):
    # Returns unpublished records for a given repo. Any list of top-level fields can be selected to return in output.


    aqparams='{"query":{"field":"publish","value":false,"jsonmodel_type":"boolean_field_query"},"jsonmodel_type":"advanced_query"}'

    records = getSearchResults(repo,aqparams)

    # Filtering based on record type (archival_objects, resources, etc.)
    if filter == None:
        records_out = records
    else:
        records_out = [ rec for rec in records if filter in rec['id'] ]

    print('Number of matching records = ' + str(len(records_out)))

    # Compile a dictionary for each record, based on which fields are requested (see defaults in def). 
    output = []
    for r in records_out:
        rec_dict = {}
        for f in fields:
            # If field is not in a record (e.g., 'publish' is not in all types) the value will be empty.
            if f in r:
                rec_dict[f] = r[f]
            else:
                rec_dict[f] = ''
        output.append(rec_dict)

    return output
 



if __name__ == '__main__':
    main()
