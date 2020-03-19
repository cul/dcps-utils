#!/bin/bash


SCRIPTNAME=`basename "$0"`
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
#TODAY=$(date +"%Y%m%d")
DT=$(date '+%d/%m/%Y %H:%M:%S')

echo "--------------"
echo $DT


/usr/bin/rsync -ave "ssh -i /home/ldpdapp/.ssh/id_dsa" /cul/cul0/ldpd/archival_data/pdfs/ ldpdapp@cunix.cc.columbia.edu:/www/data/cu/libraries/inside/projects/findingaids/scans/pdfs