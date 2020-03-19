# Script to query API for resources modified/created on a certain date


import os
import datetime
import ASFunctions as asf
from sheetFeeder import dataSheet
from datetime import datetime, date, timedelta


def main():

    asf.setServer('Prod')


    now1 = datetime.now()
    start_time = str(now1)
    end_time = '' #set later
    # today_str = str(date.today().strftime("%Y%m%d"))
    yest_str = str((date.today() - timedelta(days = 1)).strftime("%Y-%m-%d") )

    sheet_id = '198ON5qZ3MYBWPbSAopWkGE6hcUD8P-KMkWkq2qRooOY'
    data_data = [
        {'range':'resource-changes!A:Z','filter':'resources'},{'range':'accession-changes!A:Z','filter':'accessions'}
        
                ]
    

    for d in data_data:
            
        print('processing ' + d['filter'])

        the_sheet = dataSheet(sheet_id,d['range'])


        the_date = yest_str
        # the_date = '2019-08-27'
        the_repos=[2,3,4,5]
        the_fields = ['id','title','identifier','create_time','system_mtime','last_modified_by','publish']


        the_modifieds = []

        for r in the_repos:

            print('searching repo ' + str(r))

            x = asf.getByDate(r, the_date, date_type='mtime', comparator='equal', filter=d['filter'], fields=the_fields)
            for a in x:
                row = [ a[v] for v in the_fields ]
                print(row)
                the_modifieds.append(row)
                # print(list(a.values()))
                # the_modifieds.append(list(a.values()))
            print('Repo ' + str(r) + ': ' + str(len(x)))

        print('Total ' + d['filter'] + ': ' + str(len(the_modifieds)))
        # the_sheet.clear()

        # the_sheet.appendData([the_fields])
        the_sheet.appendData(the_modifieds)



    quit()





if __name__ == '__main__':
    main()
