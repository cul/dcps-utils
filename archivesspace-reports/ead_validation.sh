#!/bin/bash



DEBUG = 'True'

if [ $DEBUG == 'False']
then
    # production emails 
    mail_from=asops@library.columbia.edu
    mail_to=asops@library.columbia.edu
else
    # testing emails
    mail_from=dwh2128@columbia.edu
    mail_to=dwh2128@columbia.edu
fi


SCRIPTNAME=`basename "$0"`
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
#TODAY=$(date +"%Y%m%d")
DT=$(date '+%d/%m/%Y %H:%M:%S')

# Log file location (gets replaced with each run)
log_file=$SCRIPTPATH/../reports/${SCRIPTNAME}_log.txt


# Python virtual environment to use
py_env=$SCRIPTPATH/../pyvenv_ldpdapp

# Name of python script to run

py_script_name='validate_as_eads.py'
py_script=$SCRIPTPATH/$py_script_name

# Subject for email notification
subject="${SCRIPTNAME} is done."

# echo " " >> $log_file
# echo "=====================" >> $log_file
# echo $DT >> $log_file



echo This is an automated notification. Contact dwh2128 for more info. Script $py_script running on $(date) via $SCRIPTPATH/$SCRIPTNAME from $HOSTNAME by $USER. > $log_file

echo " " >> $log_file

echo " Synching EAD files from production server ..." >> $log_file
/usr/bin/rsync -zarvhe "ssh -i /home/ldpdapp/.ssh/id_dsa" ldpdapp@ldpd-nginx-prod1:/opt/passenger/ldpd/findingaids_prod/caches/ead_cache /cul/cul0/ldpd/archivesspace/ >> $log_file

echo " " >> $log_file

echo Setting virtual environment to $py_env. >> $log_file

echo " " >> $log_file

source $py_env/bin/activate 

echo Script output follows... >> $log_file

echo " " >> $log_file

echo "===================" >> $log_file

python $py_script &>> $log_file

echo "===================" >> $log_file

deactivate  

echo " " >> $log_file

echo Script execution complete at $(date +"%T"). >> $log_file

echo "" >> $log_file


mail -r $mail_from -s "$subject" $mail_to < $log_file





