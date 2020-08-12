import os
import datetime
import time
import csv_obtainer as csv
import process_data as pd
import html_generator as html
import email_sender as es

LOWER_TIME_LIMIT = datetime.datetime(hour=18,minute=19,second=0,microsecond=0)
UPPER_TIME_LIMIT = datetime.datetime(hour=18,minute=20,second=0,microsecond=0)
def main():
    csv.dowload_csv()
    list_of_localities = pd.get_locality_list_from_db()
    list_of_email_recipients = pd.get_recipient_list_from_db()
    pd.create_localities(list_of_localities)
    pd.read_data()
    for locality in pd.tracking_localities:
        html.create_html(locality,7)
    
    for recipient in list_of_email_recipients:
        locality_obj = pd.return_locality_obj(recipient.locality)
        es.send_mail(locality_obj, recipient.email)

def delete_clutter():
    path = 'HTML/images'
    with os.scandir(path) as dirs:
        for entry in dirs:
            os.remove(entry)

    path = 'CSVs'
    with os.scandir(path) as dirs:
        for entry in dirs:
            os.remove(entry)

    path = 'HTML'
    with os.scandir(path) as dirs:
        for entry in dirs:
            if os.path.isfile(entry):
                if entry.name == 'email_template.html':
                    continue
                os.remove(entry)

if __name__ == "__main__":
    while LOWER_TIME_LIMIT.time() < datetime.datetime.now().time() and datetime.datetime.now().time() < UPPER_TIME_LIMIT.time():
        main()
        delete_clutter()
        time.sleep(60)