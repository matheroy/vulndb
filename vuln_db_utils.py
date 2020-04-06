'''Utilities module that handles various utility processes'''


import os
import datetime
import json
import vulndb_sqllite_manage as sqlDbm

class SeedData:
    
    def __init__(self, pull_type, pull_entity):
        #pull_type values are 'url' or 'file'
        #pull_entity values are the url or the filename with the location
        self.pull_type = pull_type
        self.pull_entity = pull_entity
        self.valid_pull_types = ['file', 'url']
        self.msg = 1
        self.validate()    
        
    def validate(self):
        '''validate the pull types'''
    
        if self.pull_type not in self.valid_pull_types:
            self.msg = 'Pull type needs to be either a file or a url'
            return self.msg
        
        self.get_json_data()
        self.process_json_data()
        self.close()
    
    def get_json_data(self):
        '''function that processes json files'''
        
        if self.pull_type == 'file':
            with open(self.pull_entity) as self.file:
                self.vdata = json.load(self.file)
                
            
    def process_json_data(self):
        
        for count, item in enumerate(self.vdata['CVE_Items']):
            
            #print(f'{count}, {item} \n\n')
            print(count, item.keys())
            print(f'cve keys {item.get("cve").keys()} \n\n')
            
            self.id = item.get('cve').get('CVE_data_meta').get('ID')
            
            self.desc = item.get('cve').get('description').get('description_data')[0].get('value')
            self.severity = item.get('impact').get('baseMetricV3').get('cvssV3').get('baseSeverity')
            self.sev_score = item.get('impact').get('baseMetricV3').get('cvssV3').get('baseScore')
            self.ref_data = item.get('cve').get('references')
            self.process_references()
            self.pub_date = item.get("publishedDate") #.split('T')[0]
            
            print(self.id, self.desc)
            print(self.severity, self.sev_score)
            print(self.pub_date)
            

    def process_references(self):
        '''process to handle multiple references'''

        print(f'reference data for: {self.ref_data}')
        references = self.ref_data.get('reference_data')
        print(references)
        for reference in references:
            self.ref_url = reference.get('url')
            print(self.ref_url)
            self.save_reference()
        return


    def save_reference(self):
        '''process to save a reference to the database'''

        return

    def __repr__(self):
        return {'id': self.id, 'desc': self.desc}

    def __str__(self):
        return f'SeedData(pull_type={self.pull_type} , pull_entity={self.pull_entity})'

    def close(self):
        self.file.close()
        
    

def main():
    '''run any processess for stand alone processs'''
    DBM = sqlDbm.DbConnect()
    DB = DBM.connect()
    CURSOR = DB.cursor()

    DB.close()

if __name__ == '__main__':
    
    

    main()
