from urllib import request
import os
from pathlib import Path
from datetime import date

#Url to retrieve the current CSV file
VDoH_CSV_URL = 'https://data.virginia.gov/api/views/bre9-aqqr/rows.csv?accessType=DOWNLOAD'

def dowload_csv():
    response = request.urlopen(VDoH_CSV_URL)
    csv = response.read()
    csv_str= str(csv)
    lines = csv_str.split("\\n")
    data_dir = Path(str(os.path.dirname(__file__))+'/CSVs')
    file_path = data_dir / f'{date.today().isoformat()}.csv'
    file_writer = open(file_path,"w")
    for line in lines:
        if(line[0].isalpha()):
            line = line[2:]
        file_writer.write(line + "\n")
    file_writer.close()
