import GoogleSheetAPITools as gs
import subprocess
import re
import os


# Script to read EAD XML from two folders and populate data in two tabs of Google Sheet for comparision on various metrics.


def main():

    my_xslt = '/Users/dwh2128/Documents/ACFA/TEST/EAD_analysis/ead_qc_analysis.xsl'
    # my_files_imported = '/Users/dwh2128/Documents/ACFA/TEST/EAD_analysis/EAD-QC/EAD-imported'
    my_files_imported = '/Users/dwh2128/Documents/ACFA/TEST/ASI-49-ead_merge/Output/cleaned_eads_20190520'
    my_files_exported = '/Users/dwh2128/Documents/ACFA/exist-local/backups/for_migration/ead-export-20190520/ead_as_imported'
    saxon_path='saxon-9.8.0.12-he.jar'

    # the_sheet = '12zDzw9MdDEc-hDN9B7CFjvT4_2IV2INWX_9K-x2I83E' # 2nd import sheet
    the_sheet = '1m-4NDYLr-uLEr70AFmsDmQ0vu1pWu0568KeS0ATxv4o' # 3rd import sheet
    # the_sheet = '1YzM1dinagfoTUirAoA2hHBfnhSM1PsPt8TkwTT9KlgQ' # test sheet

    range_imported = 'imported!A:Z' 
    range_exported = 'exported!A:Z' 

    my_files = [my_files_imported,my_files_exported]
    my_targets = [range_imported,range_exported]

    # my_files = [my_files_exported]
    # my_targets = [range_exported]


    for p in range(2):

        the_file_paths = []

        for root, dirs, files in os.walk(os.path.abspath(my_files[p])):
            for file in files:
                the_file_paths.append(os.path.join(root, file))


        the_data = []

        # send any file with param to retrieve the headers as the first row.
        the_headers = saxon_process(saxon_path, the_file_paths[0], my_xslt, "header='Y'")

        the_headers = delim_to_list(the_headers,'|')
        the_data.append(the_headers)

        c = 0

        for f in the_file_paths:
            c = c + 1
            print(str(c) + " : processing" + f + "...")
            x = saxon_process(saxon_path, f, my_xslt, ' ')

            the_row = delim_to_list(x,'|')

            the_data.append(the_row)

        the_range = my_targets[p]

        gs.sheetClear(the_sheet,the_range)


        print('Writing data to Google Sheet ...')
        gs.sheetAppend(the_sheet,the_range,the_data)


def saxon_process(saxonPath, inFile, transformFile, theParams):
    cmd = 'java -jar ' + saxonPath + ' ' + inFile  + ' ' + transformFile + ' ' + theParams + ' ' + '--suppressXsltNamespaceCheck:on' 
    p = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = p.communicate()
    if result[1]: # error
        return 'SAXON ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')



def delim_to_list(the_str,the_delim):
        x = the_str.strip().decode('utf-8')
        # x = x
        the_list = x.split(the_delim)
        return the_list


if __name__ == '__main__':
    main()

