import csv
import os
from pathlib import Path
from datetime import date

#TAGS (Constants) from csv file:
DATE = "Report Date"
FIPS = "FIPS"
LOCALITY = "Locality"
DISTRICT = "VDH Health District"
TOTAL_CASES = "Total Cases"
TOTAL_HOSPITALIZATIONS = "Hospitalizations"
TOTAL_DEATHS = "Deaths"

#Global Varribles
tracking_loalities = [] #Will hold a locality objects indexed as a list

#Locality object (to store data for each area more easily)
class Locality:
    def __init__(self, name):
        self.name=name #stores the name of the locality
        self.data_list = [] #stores one day of data in each index of the list. Sorted by index
    #! index 0 is 3/17/2020 (first data), index -1 is most current data

    #tosting
    def __str__(self):
        print(self.name +':\n')
        for i in range (len(self.data_list)):
            index = str(i)
            date = self.data_list[i][DATE]
            locality = self.data_list[i][LOCALITY]
            total_cases = self.data_list[i][TOTAL_CASES]
            total_hospitalizations = self.data_list[i][TOTAL_HOSPITALIZATIONS]
            total_deaths = self.data_list[i][TOTAL_DEATHS]
            print((f'(index:{index})\t'
            + f'date:{date}\t'
            + f'locality: {locality}\t'
            + f'total_cases: {total_cases}\t'
            + f'total_hospitalizations: {total_hospitalizations}\t'
            + f'total_deaths: {total_deaths}\n'))


#Function to create the global list (tracking_loalities) localities to be tracked
def create_localities(list):
    for locality_name in list:
        tracking_loalities.insert(0, Locality(locality_name))


#This function retirives the data from the CSV file and adds the data for each localities to its objects data_list
def read_data():
    data_dir = Path(str(os.path.dirname(__file__))+'/CSVs')
    file_path = data_dir / f'{date.today().isoformat()}.csv' #todays data
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader: #Vist each line
            for locality in tracking_loalities: #Vist each locality
                if(line[LOCALITY] == locality.name): #If line is about a locality to be tracked, record the
                    #oredered dictonary (line) to the locality objects data_list
                    locality.data_list.insert(-1, line) #Data will be in date order, newest at the bottom


#Prints the raw data from the CSV debugging only
def print_raw_data_by_locality_then_year():
    for locality in tracking_loalities:
        print(locality)

#Given a List with the raw cumunlative numbers, return a list with the daily increases. index:0 is most recent day
def daily_increases_as_list(raw_data):
    #List to story daily increases
    daily_increase_list = []
    #itterate on all must last element (no data at index:-1, out of bounce)
    for i in range(len(raw_data)-1):
        #calculate daily increase. today minus yesterday
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

#Given a locality object and a catigory for a n day average to track, return a list of all n day avergae values
#The size of this must must be n less than the size of the data set
def calculate_moving_n_day_average_list(locality, tag, n):
    DAYS_TO_AVERAGE = n #Days to average over

    raw_target_data = [] #List of the data for a specific tag and locality
    for element in locality.data_list:
        raw_target_data.insert(0, element[tag])

    #Calulate daily increases
    daily_increase_list = daily_increases_as_list(raw_target_data)
    n_day_moving_average = [] #moving average list
    for i in range(len(daily_increase_list)-DAYS_TO_AVERAGE):
        current_sum = 0
        for j in range(DAYS_TO_AVERAGE):
            current_sum += daily_increase_list[i+j]

        current_n_day_average = int(round(current_sum/DAYS_TO_AVERAGE, 0))
        n_day_moving_average.insert(0, current_n_day_average)
    return n_day_moving_average

#True for today. False for yesterday
def calculate_daily_increase(locality, tag, bool):
    if bool == True:
        today_total = int(locality.data_list[-2][tag])
        yesterday_total = int(locality.data_list[-3][tag])
    else:
        today_total = int(locality.data_list[-3][tag])
        yesterday_total = int(locality.data_list[-4][tag])

    return today_total-yesterday_total

#True for this week. False for last week
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
    return round((sum/n),1)

#Reproduction Rate
def return_reproduction_rate(locality,tag,n):
    data_list = []
    for i in range (n):
        index = -2-i
        current = return_n_day_moving_average(locality,tag,n,True,index)
        previous = return_n_day_moving_average(locality,tag,n,False,index)
        r = round((current/previous),3)
        data_list.insert(0,round(r,3))
    sum = 0
    for num in data_list:
        sum += num
    return round((sum/n),3)

def return_cumlative(locality,tag):
    return locality.data_list[-2][tag]

#todo Temporary, list will be generated by email list
example_localities = ["Hampton","Virginia Beach","Newport News","Fairfax", "Loudoun", "Albemarle"] 
create_localities(example_localities)
read_data()
#print_raw_data_by_locality_then_year()
#calculate_moving_n_day_average_list(tracking_loalities[2], TOTAL_CASES, 7)
#calculate_daily_increase(tracking_loalities[2],TOTAL_CASES,False)
#return_n_day_moving_average(tracking_loalities[4],TOTAL_CASES,5,False,None)
#return_n_day_moving_average(tracking_loalities[4],TOTAL_CASES,5,True,None)
#return_reproduction_rate(tracking_loalities[4],TOTAL_CASES,10)
#print(return_cumlative(tracking_loalities[2],TOTAL_CASES))