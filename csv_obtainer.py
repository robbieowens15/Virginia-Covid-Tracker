from urllib import request
import os
from pathlib import Path
from datetime import date

#Url to retrieve the current CSV file
VDoH_CSV_URL = 'https://data.virginia.gov/api/views/bre9-aqqr/rows.csv?accessType=DOWNLOAD'

'''
This function will download the csv from a web url and save it to the directiory /CSVs
'''
def dowload_csv():
    response = request.urlopen(VDoH_CSV_URL)
    csv = response.read()
    csv_str= str(csv)
    lines = csv_str.split("\\n")

    data_dir = Path(str(os.path.dirname(__file__))+'/CSVs')

    #Save file with todays date
    file_path = data_dir / f'{date.today().isoformat()}.csv'

    file_writer = open(file_path,"w")
    for line in lines:
        #if/else is for the first line to remove a "'b" and the
        #"/r" at the end of every line. Makes reading easier
        
        if(line[0].isalpha()):
            line = line[2:]
    
        file_writer.write(line + "\n")
    file_writer.close()

#Uncomment and run file to retireve latest data
dowload_csv()