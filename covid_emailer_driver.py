import csv_obtainer as csv
import process_data as pd
import html_generator as html
import email_sender as es

def main():
    csv.dowload_csv()
    #todo This Should come from form
    pd.create_localities(pd.example_localities)
    pd.read_data()
    for locality in pd.tracking_loalities:
        html.create_html(locality,7)
    es.send_mail(pd.tracking_loalities[2])

#def delete_clutter():

if __name__ == "__main__":
    main()
    
    