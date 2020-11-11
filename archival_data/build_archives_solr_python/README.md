# build_archives_solr.py
## Purpose
This python script builds the solr index for the archives portal and oral history portal via an xslt transformation of MARC-XML outputs generated upstream.
## Requirements
This script was developed and tested using Python 2 on the test nginx servers.

## Setup
### Saxon 9
The script expects that there is a Saxon 9 jar file at `~/lib/saxon-9he.jar`
### Source MARC-XML
The script expects files named by repository code in `/cul/cul0/ldpd/archival_data/marc/archives_portal`
The script also expects a writable directory at `/cul/cul0/ldpd/archival_data/marc/oral_history_portal` where it will capture the output of `/cul/cul0/ldpd/ccoh/fetchOralHistoryRecords`

## Usage
The script takes as argument a comma-delimited list of solr environments. For example:
```bash
python ~/bin/diag-utils/build_archives_solr_python/build_archives_solr.py dev,test
```
## Testing the script
Currently, there is no automated testing of the script.