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

class InitDB:
    
    def __init__(self, initialize=None):
        
        self.initialize = initialize
        if self.initialize != None:
            self.initialize_db()

    def initialize_db(self):
        '''initialize the sqlite3 database'''

        logger.info('Initializing the database')
        self.status = 1
        try:
            self.drop_items()
        except:
            pass
        finally:
            try:
                self.create_tables()
                self.create_indexes()
            except Exception as err:
                logger.warning(f'Error in {__name__}: {err}')
                self.status = 0

        return self.status
        
    def create_tables(self):
        '''function to create the base tables needed for the program'''

        logger.info('creating new tables')
        self.status = 1
        try:
            CURSOR.execute(
                '''CREATE TABLE job_run_check(id INTEGER PRIMARY KEY NOT NULL,
                run_date TEXT NOT NULL, run_time TEXT NOT NULL, last_modified TEXT NOT NULL,
                data_size integer NOT NULL, file_type TEXT, file_size integer)
                ''')
            DB.commit()

            CURSOR.execute(
                '''CREATE TABLE vulnerabilities(id INTEGER NOT NULL,
                year TEXT NOT NULL, cveid TEXT PRIMARY KEY NOT NULL, description TEXT NOT NULL,
                severity TEXT NOT NULL, sev_score TEXT NOT NULL, pub_date TEXT NOT NULL)
                ''')
            DB.commit()

            CURSOR.execute(
                '''CREATE TABLE reference_data(id INTEGER NOT NULL,
                cveid TEXT PRIMARY KEY NOT NULL, reference_links TEXT NOT NULL)
                ''')
            DB.commit()
            
        except Exception as err:
                logger.info(err)
                self.status = 0
                
        return self.status

    def create_indexes(self):

        logger.info('creating new indexes')
        CURSOR.execute(
            '''CREATE UNIQUE INDEX id_idx on vulnerabilities(id)''')
        DB.commit()

        CURSOR.execute(
            '''CREATE INDEX cveid_idx on vulnerabilities(cveid)''')
        DB.commit()

        CURSOR.execute('''CREATE INDEX ref_cveid_idx on reference_data(cveid)''')
        DB.commit()

        return

    def drop_list(self, item_list, item_type):
        '''drop any existing tables or indexes'''
        
        self.item_type = item_type
        self.item_list = item_list
        for item in self.item_list:
            try:
                CURSOR.execute(f'''DROP {self.item_type} {item}''')
                DB.commit()
            except Exception as err:
                logger.info(err)
                pass
        return

    def drop_items(self):
        '''function to drop assests from the database'''

        self.table_list = ['job_run_check', 'vulnerabilities', 'reference_data']
        self.index_list = ['id_idx', 'cveid_idx', 'ref_cveid_idx']

        self.drop_list(self.table_list, 'TABLE')
        self.drop_list(self.index_list, 'INDEX')

        return


class LoadData:
    
    def __init__(self):
        super().__init__()

    def check_job_run(self, ins_data=1):
        if ins_data == 1:
            CURSOR.execute(
            '''insert into job_run_check(id, run_date, run_time, last_modified,
                data_size, file_type, file_size) values(?, ?, ?, ?, ?, ?, ?)
                '''), (1, self.today, self.time, self.meta_date, self.data_size,
                       self.type, self.file_type)
            DB.commit()
        else:
            CURSOR.execute('update job_run_check set run_time=? where run_date=?', 
                           (self.time, self.today))

    def insert_vulnerabilities(self):

        CURSOR.execute(
            '''insert into vulnerabilities(id, year, cveid, description,
            severity, sev_score, pub_date) 
            values(?, ?, ?, ?, ?, ?, ?)'''), (self.count, '2020', self.id, self.desc,
                                              self.severity, self.sev_score, self.pub_date)
        DB.commit()

    def insert_reference_data(self):
        CURSOR.execute(
            '''insert into reference_data(id, cveid, reference_links)
            values( ?, ?, ? )'''), (self.count, self.id, self.url)
        DB.commit()

    def update_vulnerabilities(self):
        '''update the vulnerabiliites table'''
        pass
        
    
    def update_reference_data(self):
        '''update reference data table'''
        pass
    

def main():

    logger.info('In sqlitemanage module')
    newDb = InitDB(1)
    #test_dbm()

    return


if __name__ == '__main__':

    
    DBM = DbConnect()
    DB = DBM.connect()
    CURSOR = DB.cursor()

    main()
    DB.close()
