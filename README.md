# DCPS-UTILS

This is a repo for DCPS scripts and utilities. Contact dwh2128 for questions/info. 

## Use

This repo is git deployed to service server via post-receive hook. Do not make changes to files in situ on server; they will be overwritten.

## Overview

### resources dir

This has a few things of general use for many scripts. 

#### python_wrapper.sh

This is a bash script used to set Python environment, run a Python script, log results to file, and optionally send log notification to users upon completion. A distinct notification is sent if an error is returned from the Python script.

*Use from shell*

```
nohup ./resources/python_wrapper.sh [options] <path to python script> &
```

*Options*

* -t: test mode
* -s: silent mode (no notifications sent unless error)
* -h: help

#### pyvenv_ldpdapp

Python virtual environment (venv), used by python_wrapper. Activate with source ./resources/pyvenv_ldpdapp/bin/activate

(Note: this is not maintained in git repo but needs to be in deploy for scripts to work.)

#### XML tools

* saxon - xslt processor
* jing - schema validator

### archivesspace folder

Many tools for interacting with ArchivesSpace via the API. Main tool sets are:

* ASFUnctions.py - collection of frequently used API functions
* dcps_utils.py - some reusable functions
* sheetFeeder.py - library for interacting with Google Sheets API

### archival_data folder

Scripts for processing archival data outside of ArchivesSpace, e.g., Voyager-to-Solr for Archives Portal and Oral History Portal.
