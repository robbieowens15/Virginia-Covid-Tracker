import os

import csv_obtainer as csv
import process_data as pd
import html_generator as html
import email_sender as es

def main():
    csv.dowload_csv()

    #todo This Should come from form
    pd.create_localities(pd.example_localities)

    pd.read_data()

    for locality in pd.tracking_localities:
        html.create_html(locality,7)
    es.send_mail(pd.tracking_localities[1])

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
    main()
    delete_clutter()
    
    