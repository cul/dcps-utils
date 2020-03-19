#!/bin/bash


# python3 pypypy.py > error_catcher.stdout 2> error_catcher.sterr

PYTHON_ERROR=false
STDERR=''
STDOUT=''

# if RESULT=$(python3 pypypy.py 2>&1); then
#     STDOUT=$RESULT
# else
#     rc=$?
#     PYTHON_ERROR=true
#     STDERR=$RESULT
# fi

# if $PYTHON_ERROR; then
#     echo 'There was an error!'
#     echo "$STDERR"
# fi

# echo "$STDOUT"




function python_exec()
{
    PYTHON_ERROR=false
    STDERR=''
    STDOUT=''
    local OUTPUT
    local RESULT
    if RESULT=$(python3 $1 2>&1); then
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


python_exec pypypy.py

if $PYTHON_ERROR; then
    echo '*************There was an error!'
    echo "$STDERR"
else
    echo "$STDOUT"
fi

echo $email_subject


