'''main module for the vulnerability database application'''

import os
import datetime
import requests
from vuln_db_logger import logger
import vulndb_sqllite_manage as sqlDbm

# instantiate the database connection as globals
DBM = sqlDbm.DbConnect()
DB = DBM.connect()
CURSOR = DB.cursor()

def main():
    '''main module'''

    pass



if __name__ == '__main__':

    logger.info('Starting up the main module')
    main()
    
    


