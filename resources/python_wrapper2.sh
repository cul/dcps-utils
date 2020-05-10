#!/bin/bash

# Generic wrapper for running Python scripts using a virtual environment and sending log to designated recipient.
#
# Put python script name in first argument when running, e.g., 
# nohup ./python_wrapper.sh /path/to/script.py &
#
# Run in "test mode":
# nohup ./python_wrapper.sh -t /path/to/script.py &


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
    \? ) echo "Usage: cmd [-t] [-h] [-p] <python script path>"
    ;;
      
  esac
done

# Shift args so filename will be $1 with or without flags
shift $((OPTIND -1))

# emails for production use -- may be overridden by -t flag
mail_from=asops@library.columbia.edu
mail_to=asops@library.columbia.edu


case "$myOpt" in 

        testMode) 
                # Switch to test mode (don't send notifications to alias)
                mail_from=dwh2128@columbia.edu
                mail_to=dwh2128@columbia.edu
                        ;;
        productionMode) 
                # Switch to production mode (don't send notifications to alias)
                # Options already set by default; don't do anything.
                        ;;
        helpMe) 
                # process URL grep
                echo "Usage: cmd [-t] [-h] <python script path>"

esac


function python_exec()
# Function to execute a python script (arg1) and distinguish any errors from stdout  
{
    PYTHON_ERROR=false
    STDERR=''
    STDOUT=''
    local OUTPUT
    local RESULT
    if RESULT=$(python $1 2>&1); then
        STDOUT="$RESULT"
        # OUTPUT="$RESULT"
    else
        rc=$?
        PYTHON_ERROR=true
        STDERR="$RESULT"
        # OUTPUT="$STDERR"
    fi

    # return "$OUTPUT"
}



# Get info of this script
SCRIPTNAME=`basename "$0"`
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

# Python virtual environment to use
py_env=$SCRIPTPATH/pyvenv_ldpdapp

# Name of python script to run
py_script=$1
py_script_name=`basename "$1"`

# Log file location (gets replaced with each run)
log_file=$SCRIPTPATH/reports/${py_script_name}_log.txt


####

echo This is an automated notification. Contact dwh2128 for more info. Script $py_script running on $(date) via $SCRIPTPATH/$SCRIPTNAME from $HOSTNAME by $USER. > $log_file

echo " " >> $log_file

echo Setting virtual environment to $py_env. >> $log_file

echo " " >> $log_file

source $py_env/bin/activate 

echo Script output follows... >> $log_file

echo " " >> $log_file

echo "===================" >> $log_file


# python $py_script &>> $log_file
python_exec $py_script


# Check if there were errors, and set the subject line accordingly
if $PYTHON_ERROR; then
    REP=true
    subject="ERROR: ${py_script_name} encountered a problem!"
    echo "$STDERR" &>> $log_file
elif [ -n "$STDOUT" ] ; then
    REP=true
    subject="${py_script_name} is done."
    echo "$STDOUT" &>> $log_file
else
    REP=false
    subject="${py_script_name} NO OUTPUT."
    echo "(No script output)"  &>> $log_file
fi

echo "===================" >> $log_file


deactivate  

echo " " >> $log_file

echo Script execution complete at $(date +"%T"). >> $log_file

echo "" >> $log_file

if $REP ; then
    mail -r $mail_from -s "$subject" $mail_to < $log_file
fi


