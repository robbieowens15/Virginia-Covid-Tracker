import csv
import os
from pathlib import Path
from datetime import date
import csv_obtainer

import sys
sys.path.insert(1,'/flask_email_signup')
from flask_email_signup import db, modles

DATE = "Report Date"
FIPS = "FIPS"
LOCALITY = "Locality"
DISTRICT = "VDH Health District"
TOTAL_CASES = "Total Cases"
TOTAL_HOSPITALIZATIONS = "Hospitalizations"
TOTAL_DEATHS = "Deaths"

tracking_localities = [] 
all_localities = []

class Locality:
    def __init__(self, name):
        self.name=name 
        self.data_list = []

def get_recipient_list_from_db():
    recipient_list = []
    recipient_list = modles.Recipient.return_all_recipients()
    return recipient_list

def get_locality_list_from_db():
    locality_list = []
    recipient_list = modles.Recipient.return_all_recipients()
    for recipient in recipient_list:
        if not recipient.locality in locality_list:
            locality_list.insert(-1,recipient.locality)
    return locality_list

def return_locality_obj(locality_str):
    for locality in tracking_localities:
        if locality.name == locality_str:
            return locality

def create_localities(list):
    for locality_name in list:
        tracking_localities.insert(0, Locality(locality_name))

def read_data():
    data_dir = Path(str(os.path.dirname(__file__))+'/CSVs')
    file_path = data_dir / f'{date.today().isoformat()}.csv'
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader: 
            if not line[LOCALITY] in all_localities:
                all_localities.insert(0,line[LOCALITY])
            for locality in tracking_localities:
                if line[LOCALITY] == locality.name:
                    locality.data_list.insert(-1, line)

def daily_increases_as_list(raw_data):
    daily_increase_list = []
    for i in range(len(raw_data)-1):
        today = 0
        yesterday = 0
        try:
            today = int(raw_data[i])
        except:
            today = 0
        try:
            yesterday = int(raw_data[i+1])
        except:
            yesterday = 0
        daily_increase = today - yesterday
        #check for nonsensical data
        if daily_increase < 0:
            daily_increase = 0
        daily_increase_list.insert(0, daily_increase)
    return daily_increase_list

def calculate_moving_n_day_average_list(locality, tag, n):
    DAYS_TO_AVERAGE = n 

    raw_target_data = []
    for element in locality.data_list:
        raw_target_data.insert(0, element[tag])

    daily_increase_list = daily_increases_as_list(raw_target_data)
    n_day_moving_average = []
    for i in range(len(daily_increase_list)-DAYS_TO_AVERAGE):
        current_sum = 0
        for j in range(DAYS_TO_AVERAGE):
            current_sum += daily_increase_list[i+j]

        current_n_day_average = int(round(current_sum/DAYS_TO_AVERAGE, 0))
        if current_n_day_average < 0:
            current_n_day_average = 0
        n_day_moving_average.insert(0, current_n_day_average)

    return n_day_moving_average

def calculate_daily_increase(locality, tag, bool):
    if bool == True:
        today_total = int(locality.data_list[-2][tag])
        yesterday_total = int(locality.data_list[-3][tag])
    else:
        today_total = int(locality.data_list[-3][tag])
        yesterday_total = int(locality.data_list[-4][tag])

    if today_total-yesterday_total < 0:
        return 0
    else:
        return today_total-yesterday_total

def return_n_day_moving_average(locality,tag,n,bool,index=None):
    data_list = []
    if index is None:
        index = -2
    if bool == False:
        index -= n
    for i in range(n):
        data = int(locality.data_list[index][tag])-int(locality.data_list[index-1][tag])
        data_list.insert(0,data)
        index -= i
    sum = 0
    for num in data_list:
        sum += num
    if round((sum/n),1) > 0:
        return round((sum/n),1)
    else:
        return 0.0

def return_reproduction_rate(locality,tag,n):
    data_list = []
    for i in range (n):
        index = -2-i
        current = return_n_day_moving_average(locality,tag,n,True,index)
        previous = return_n_day_moving_average(locality,tag,n,False,index)
        if previous == 0:
            r = 0
        else:
            r = round((current/previous),3)
        data_list.insert(0,round(r,3))
    sum = 0
    for num in data_list:
        sum += num
    return round((sum/n),3)

def return_cumlative(locality,tag):
    return locality.data_list[-2][tag]


