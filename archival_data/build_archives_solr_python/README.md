# build_archives_solr.py
## Purpose
This python script builds the solr index for the archives portal and oral history portal via an xslt transformation of MARC-XML outputs generated upstream.
## Requirements
Python 3. Reporting (via digester.py script) requires sheetFeeder library. Run in virtual Python environment (/opt/dcps/resources/pyvenv_ldpdapp).

## Setup
### Saxon 9
The script expects that there is a Saxon 9 jar file in `/opt/dcps/resources/`
### Source MARC-XML
The script expects archives portal XML files nightly from Voyager named by repository code in `/cul/cul0/ldpd/archival_data/marc/archives_portal`
The script also expects a writable directory at `/cul/cul0/ldpd/archival_data/marc/oral_history_portal` where it will capture the output of the Perl script `fetchOralHistoryRecords`
### Environment
The Perl script `fetchOralHistoryRecords` relies on the PERL library path:
```bash
PERL5LIB=\
/home/ldpdapp/share/perl5:\
/home/ldpdapp/share/perl5/CPAN:\
/home/ldpdapp/lib/perl5:\
/home/ldpdapp/lib/perl5/site_perl:\
/home/ldpdapp/lib64/perl5:\
/home/ldpdapp/lib64/perl5/site_perl:
```
If run on cron use python_wrapper.sh with -e flag set to load home env on execution.

## Usage
The script takes as argument a comma-delimited list of solr environments. For example:
```bash
python3 /opt/dcps/archival_data/build_archives_solr_python/build_archives_solr.py dev,test
```

To run with wrapper:
```bash
/opt/dcps/resources/python_wrapper.sh -es /opt/dcps/archival_data/build_archives_solr_python/build_archives_solr.py dev,test
```

## Testing the script
Currently, there is no automated testing of the script.