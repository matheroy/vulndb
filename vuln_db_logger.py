'''manage all app based logs via logging module'''

import os
import datetime
import logging

TODAY = datetime.datetime.today()
TIMESTAMP = f'{TODAY.month}-{TODAY.day}-{TODAY.year}'

LOG_FILE_LOC = f'{os.getcwd()}\\logs'
LOG_FILE_NAME = f'vuln_db_{TIMESTAMP}.log'
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
LOG_FILE = f'{LOG_FILE_LOC}\\{LOG_FILE_NAME}' # logging module will auto create if not found
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()
logger.info("vuln_db log Startup")

