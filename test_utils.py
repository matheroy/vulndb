'''test file for utilities'''

import os
import vuln_db_utils as vu 

file = 'nvdcve-test.json'
file2 = 'nvdcve-1.1-2020.json'
filename = f'{os.getcwd()}\\data\\nvdcve-1.1-2020.json\\{file}' 

#vu.process_json_data(filename)

def run():
    seed_data = vu.SeedData('file', filename)
    #print(seed_data)
    
    return print(seed_data)


if __name__ == '__main__':
    run()
    

