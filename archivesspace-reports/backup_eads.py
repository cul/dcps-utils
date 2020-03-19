import subprocess
import os
import re
from datetime import datetime, date, timedelta


def main():


    my_name = __file__

    # This makes sure the script can be run from any working directory and still find related files.
    my_path = os.path.dirname(__file__)

    yest_str = str((date.today() - timedelta(days = 1)).strftime("%Y%m%d") )



    print('====== Syncing files from production cache... ======')
    print(' ')


    keyPath = ""

    fromPath = '/cul/cul0/ldpd/archivesspace/ead_cache/*'
    toPath = '/opt/dcps/archivesspace/output/ead/' + yest_str 

    myOptions = "--exclude 'clio*'"

    x = rsync_process(keyPath,fromPath,toPath,myOptions)
    print(x)


    print(' ')


    quit()




def rsync_process(keyPath, fromPath, toPath, options):
    if keyPath:
        cmd = '/usr/bin/rsync -zarvhe "ssh -i ' + keyPath + '" ' + options + ' ' + fromPath + ' ' + toPath 
    else:
        cmd = '/usr/bin/rsync -zavh ' + options + ' ' + fromPath + ' ' + toPath 

    print('Running command: ' + cmd + ' ...')
    print(' ')

    result = subprocess.Popen([cmd], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()

    if result[1]: # error
        return 'RSYNC ERROR: ' + str(result[1].decode('utf-8'))
    else:
        return result[0].decode('utf-8')





if __name__ == '__main__':
    main()
