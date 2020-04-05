'''Module that sets up and manages the sqlite database'''

import os
import sys
import sqlite3
import pickle
import datetime
from vuln_db_logger import logger

DB_FILE_LOC = f'{os.getcwd()}\\data'
DB_FILE_NAME = f'vuln_db.s3db'
VULN_DB = f'{DB_FILE_LOC}\\{DB_FILE_NAME}'

class DbConnect:

    def __init__(self, env='prod'):
        self.env = env

    def connect(self):
        self.conn = sqlite3.connect(VULN_DB)
        return self.conn

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()


def create_tables():
    '''function to create the base tables needed for the program'''

    status = 1
    try:
        cursor.execute(
            '''CREATE TABLE job_run_check(id INTEGER PRIMARY KEY NOT NULL,
            checked_date TEXT NOT NULL, checked_time TEXT NOT NULL, last_modified TEXT NOT NULL,
            data_size integer NOT NULL, file_type TEXT, file_size integer)
            ''')
        db.commit()

        cursor.execute(
            '''CREATE TABLE vulnerabilities(id INTEGER PRIMARY KEY NOT NULL,
            year TEXT NOT NULL, cveid TEXT NOT NULL, description TEXT NOT NULL,
            cvss TEXT NOT NULL, pub_date TEXT NOT NULL)
            ''')
        db.commit()

        cursor.execute(
            '''CREATE TABLE reference_data(id INTEGER PRIMARY KEY NOT NULL,
            cveid TEXT NOT NULL, reference_links TEXT NOT NULL)
            ''')
        db.commit()
        
    except:
            status = 0
            
    return status

def create_indexes():

    cursor.execute(
        '''CREATE UNIQUE INDEX id_idx on vulnerabilities(id)''')
    db.commit()

    cursor.execute(
        '''CREATE INDEX cveid_idx on vulnerabilities(cveid)''')
    db.commit()

    cursor.execute('''CREATE INDEX ref_cveid_idx on reference_data(cveid)''')
    db.commit()

    return

def drop_list(item_list, item_type):

    for item in item_list:
        try:
            cursor.execute(f'''DROP {item_type} {item}''')
            db.commit()
        except:
            pass
    return

def drop_items():
    '''function to drop assests from the database'''

    table_list = ['job_run_check', 'vulnerabilities', 'reference_data']
    index_list = ['id_idx', 'cveid_idx', 'ref_cveid_idx']

    drop_list(table_list, 'TABLE')
    drop_list(index_list, 'INDEX')

    return


def insert_data(page_id, pickled_data, log_name):

    cursor.execute(
        '''insert into Books_list(id, pickled_data, data_file_name)
        values(?, ?, ?)''', (page_id, pickled_data, log_name))
    db.commit()

    return

def initialize_db():
    '''initialize the sqlite3 database'''

    status = 1
    try:
        drop_items()
    except:
        pass
    finally:
        try:
            create_tables()
            create_indexes()
        except Exception as err:
            logger.warning(f'Error in {__name__}: {err}')
            status - 0
    
    return status

def update_data(pList):
    '''update the data'''

    cursor.execute(
        '''update pickled_Books set pickled_data = ? where id=?''', (1, pList))
    db.commit()

    return


def main():

    initialize_db()
    #test_dbm()

    return


if __name__ == '__main__':

    dbm = DbConnect()
    db = dbm.connect()
    cursor = db.cursor()

    main()
    db.close()
