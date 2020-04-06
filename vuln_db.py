'''main module for the vulnerability database application

The app is expected to run in a python 3, specifically 3.65+ environment

1. Please run the db initialization process to create the sqllite3 database
python vulndb_sqllite_manage.py

2. Run the application using the Flask service
python vuln_db.py 

The flask service will allow for api requests to be made.  The simple home page provides, the call methods

3.The app will auto check to see if the database has data, if so then updates will
be managed by a sleeper function

Once the app is installed/cloned, it will auto create the data and logs directory which is where the app will look for 
it's data directory (input files, databases), and log file (logs directory) respectively 

'''

import os
import time
import datetime
import requests
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from vuln_db_logger import logger
import vulndb_sqllite_manage as sqlDbm
from vuln_db_utils import *

# instantiate the database connection as globals
DBM = sqlDbm.DbConnect()
DB = DBM.connect()
CURSOR = DB.cursor()
zip_link = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2020.json.zip'
zip_meta_link = 'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2020.meta'

file = 'nvdcve-test.json'
file2 = 'nvdcve-1.1-2020.json'
filename = f'{os.getcwd()}\\data\\nvdcve-1.1-2020.json\\{file}'
PORT = '9000'

app = Flask(__name__)


@app.route('/')
def hello():
    msg = f'Welcome to the local Vulnerability Checker \
        This app supports the following api requests \
        \\getCVEID \
        \\getsev_score \
        \\getPubDate '
    return msg


@app.route('/getCVEID')
def get_cve_id():

    # implement the service to pull data from the datbase
    msg = {'cve': {
           'id': 'CVE-2020-0010',
           'desc': 'In fpc_ta_get_build_info of fpc_ta_kpi.c, there is a possible out of \
                    bounds write due to a missing bounds check. This could lead to local escalation \
                    of privilege with System execution privileges needed. User interaction is not \
                    needed for exploitation.Product: AndroidVersions: \
                    Android kernelAndroid ID: A-137014293References: N/A',
           'reference_link': 'https://source.android.com/security/bulletin/2020-03-01'}}
    
    return msg #jsonify(msg)


@app.route('/getSev_score')
def get_sev_score():
    # implement the service to pull data from the datbase
    msg = {'cve': {
           'id': 'CVE-2020-0010',
           'severity': 'MEDIUM',
           'sev_score': '6.7'}}

    return msg 


@app.route('/getPubDate')
def get_sev_score():
    # implement the service to pull data from the datbase
    msg = {'cve': {
           'id': 'CVE-2020-0010',
           'published_date': '2020-01-08T19:15Z'}}

    return msg


def main():
    '''main module'''

    last_run = Sleep()
    if last_run.job_run == None:
        seed_data = SeedData('file', file)
    else:
        # call the sleep timeout method if the time is past the last run time
        pass
    


if __name__ == '__main__':

    logger.info('Starting up the main module')
    app.run(port=PORT)
    main()
    
    


