# DCPS-UTILS

This is a repo for DCPS scripts and utilities. Contact dwh2128 for questions/info. 

## Use

This repo is git deployed to service server via a post-receive hook located in ~/git-deploy/dcps-utils. Do not make changes to files in situ on server; they will be overwritten on deploy.

### Deploy

Set up a production remote in local git: 

 production --> ldpdserv@service:/home/ldpdserv/git-deploy/dcps-utils

When on the `development` branch, a push will deploy commits to the dcps-utils-dev folder:

```
git push production development
```

When on `master`, a push will deploy to dcps-utils folder. 

```
git push production master
```

Make changes in `development` first and deploy to the dev folder to try out scripts and run tests before making them available to crontab via master.

You can also set up a `test` remote pointing to service-test, where code will be deployed to symetric folders there for testing purposes.

## Overview

### resources directory

This has a few things of general use for many scripts. 

#### python_wrapper.sh

This is a bash script used to set Python environment with dependencies, run a Python script, log results to file, and optionally send log notification to users upon completion. A distinct notification subject is sent if an error is returned from the Python script.

*Use from shell*

```
nohup ./resources/python_wrapper.sh [options] <path to python script> &
```

*Options*

* -t: test mode
* -s: silent mode (no notifications sent unless error)
* -e: load user environment vars before running (e.g., in ~/.bashrc)

#### Virtual environment: pyvenv_ldpdserv

Python virtual environment (venv) activated by python_wrapper. Activate manually with source ./resources/pyvenv_ldpdapp/bin/activate

(Note: this is not maintained in git repo but needs to be in deploy for scripts to work.)

See requirements_ldpdserv.txt for dependencies.

The virtual env also contains a path configuration file in <venv_root>/lib/python3.4/site-packages/ called dcps-resources.pth that adds resources/shared_libraries to PYTHONPATH. This a python script from anywhere in the project to import local libraries (e.g., dcps-utils.py) from this location (see below).

#### shared_libraries

Folder of python resources made available to scripts via the addition to PYTHONPATH in dcps-resources.pth (see above). The required libraries include:

* ASFUnctions.py - collection of frequently used API functions
* dcps_utils.py - some reusable functions
* sheetFeeder.py - library for interacting with Google Sheets API
* digester.py - library for reporting script events for daily email digest.

#### reports

The output location for python_wrapper.py log output.

#### XML tools

* saxon - xslt processor
* jing - schema validator

### archivesspace folder

tools for interacting with ArchivesSpace via the API. M

#### as_crons

Scripts that are run on crons for reporting, integrations, etc.

#### as_reports

Scripts to extract data for various reporting purposes other than those on crons.

#### as_tools

Scripts to manipulate ArchivesSpace data or otherwise interact with it.

#### xslt

XSLT stylesheets used by scripts to transform XML data for various purposes, e.g., to prepare the OAI-PMH output from AS for import into Voyager.

#### tests

Tests of various script functions using PyTest. All tests are run on a cron and can also be done from the command line using:

```
/opt/dcps/resources/pyvenv_ldpdserv/bin/pytest /opt/dcps/dcps-utils --disable-pytest-warnings
```

Tests should be rerun whenever updates are deployed.

### archival_data folder

Scripts for processing archival data outside of ArchivesSpace, e.g., Voyager-to-Solr for Archives Portal and Oral History Portal.

#### build_archives_solr_python

This is a duplicate of the code managed in [diag-utils](https://github.com/cul/diag-utils/tree/master/build_archives_solr_python) and is here for deployment simplicity. The script runs on crons for DEV, TEST, and PROD nightly.
