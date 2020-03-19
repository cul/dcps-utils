#!/bin/bash


SCRIPTNAME=`basename "$0"`
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
#TODAY=$(date +"%Y%m%d")
DT=$(date '+%d/%m/%Y %H:%M:%S')

echo "--------------"
echo $DT

/usr/bin/rsync -zarvhe "ssh -i /home/ldpdapp/.ssh/id_dsa" ldpdapp@ldpd-nginx-prod1:/opt/passenger/ldpd/findingaids_prod/caches/ead_cache /cul/cul0/ldpd/archivesspace/

