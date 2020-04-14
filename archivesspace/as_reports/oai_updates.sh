#!/bin/bash

# Script to extract a list of records from the nightly OAI harvest "delta" file, and push the results to /cul/cul0/ldpd/archivesspace/updates/ for consumption by the finding aid Web application.


SCRIPTNAME=`basename "$0"`
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"


# Generalizable option handler

while getopts ":tph" opt; do
  case ${opt} in
    t ) # process option t
    myOpt=testMode
      ;;
    p ) # process option p
    myOpt=productionMode
      ;;
    h ) # process option h
    myOpt=helpMe
    # echo "Help me!"
      ;;
    \? ) echo "Usage: cmd [-t] [-h] [-p]"
    ;;
      
  esac
done

# Shift args so filename will be $1 with or without flags
shift $((OPTIND -1))

# vars for production use -- may be overridden by -t flag
    mail_from=asops@library.columbia.edu
    mail_to=asops@library.columbia.edu
    today=$(date +"%Y%m%d")
    # yesterday=$(date --date="yesterday" +"%Y%m%d")
    # source_dir=/cul/cul0/lito/libsys/voyager/prod/data/loads/AS_harvest
    source_dir=/cul/cul0/ldpd/archivesspace/oai
    delta_output_dir=/cul/cul0/ldpd/archivesspace/updates
    reports_dir=/opt/dcps/resources/reports

case "$myOpt" in 

        testMode) 
                # Switch to test mode (don't send notifications to alias)
                today=20190906
                mail_from=dwh2128@columbia.edu
                mail_to=dwh2128@columbia.edu
                source_dir=/cul/cul0/lito/libsys/voyager/prod/data/loads/AS_harvest
                delta_output_dir=$SCRIPTPATH/output
                reports_dir=$SCRIPTPATH/../reports
                        ;;
        productionMode)  
                # Switch to production mode
                # Options already set by default; don't do anything.
                        ;;
        helpMe) 
                # process URL grep
                echo "Usage: use -t for Test Mode, -p (default) for Production mode"
esac




subject="${SCRIPTNAME} is done."


xsl_file1=$SCRIPTPATH/extract-bibids.xsl
xsl_file2=$SCRIPTPATH/generateLookupTable.xsl

saxon_jar=/opt/dcps/resources/saxon-9.8.0.12-he.jar

 
# delta_in_file=${today}.asDeltaRaw.xml
# delta_in_file=${today}.asRaw.xml
delta_in_file=${today}.asClean.xml
delta_out_file=${today}.asDeltaIDs.csv
# all_in_file=${today}.asAllRaw.xml
all_in_file=${today}.asRaw.xml
all_out_file=id_lookup_prod.csv

log_file=$reports_dir/${SCRIPTNAME}_log.txt

echo This is an automated notification. Contact dwh2128 for more info. Script $SCRIPTNAME running on $(date) by $SCRIPTPATH/$SCRIPTNAME from $HOSTNAME. > $log_file

echo " " >> $log_file

# Run through Saxon with filename as parameter, for output to notification.
# Note: xsl:message does not go to stdout! Must use &>> to append all output.
java -cp $saxon_jar net.sf.saxon.Transform -xsl:$xsl_file1 -o:$delta_output_dir/$delta_out_file -s:$source_dir/$delta_in_file filename=$delta_in_file &>> $log_file

echo " " >> $log_file

echo Saving XML output to $delta_output_dir/$out_file. >> $log_file

echo " " >> $log_file


### NOTE: Commenting this out for now as there is no longer an "allRaw" file to read from.

echo Generating new lookup table at $SCRIPTPATH/$all_out_file ... >> $log_file
echo " " >> $log_file

java -cp $saxon_jar net.sf.saxon.Transform -xsl:$xsl_file2 -o:$SCRIPTPATH/$all_out_file -s:$source_dir/$all_in_file &>> $log_file

echo " " >> $log_file



echo Script execution complete at $(date +"%T"). >> $log_file

echo "" >> $log_file


mail -r $mail_from -s "$subject" $mail_to < $log_file




