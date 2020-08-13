import os
from os import environ
import imghdr
from datetime import date
import smtplib, ssl
from email.message import EmailMessage
import process_data as pd

import sys
sys.path.insert(1,'/flask_email_signup')
from flask_email_signup import db, modles

date = date.today().isoformat()

def send_mail(locality, to_address):
    message = EmailMessage()
    message['subject'] = "COVID 19 Update"
    message['from'] = 'covidvirginia@gmail.com'
    message['to'] = to_address
    message.set_content('Enable HTML to view this message')
    html_message = open(f'HTML/{locality.name}-{date}.html').read()
    message.add_alternative(html_message, subtype='html')
    with open(f'HTML/images/{locality.name}-7daymovingTotal Cases-{date}.jpg','rb') as attach_file:
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'New Cases vs Time {locality.name} {date}')
    with open(f'HTML/images/{locality.name}-7daymovingHospitalizations-{date}.jpg','rb') as attach_file:
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'New Hospitalizations vs Time {locality.name}  {date}')
    with open(f'HTML/images/{locality.name}-7daymovingDeaths-{date}.jpg','rb') as attach_file:
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'New Deaths vs Time {locality.name}  {date}')

    with open(f'HTML/images/{locality.name}-cumvstimeTotal Cases-{date}.jpg','rb') as attach_file:
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'Total Cases vs Time {locality.name}  {date}')

    with open(f'HTML/images/{locality.name}-cumvstimeHospitalizations-{date}.jpg','rb') as attach_file:
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'Total Hospitalizations vs Time {locality.name}  {date}')

    with open(f'HTML/images/{locality.name}-cumvstimeDeaths-{date}.jpg','rb') as attach_file:
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'Total Deaths vs Time {locality.name}  {date}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(environ.get('COVID_EMAIL'), environ.get('COVID_EMAIL_PASSWORD'))
        smtp.send_message(message)

def send_admin_email(to_address):
    message = EmailMessage()
    message['subject'] = "ADMIN: COVID 19 Flask Rundown"
    message['from'] = 'covidvirginia@gmail.com'
    message['to'] = to_address

    line=""

    locality_to_num_viewers_dict = {}
    recipient_list = modles.Recipient.return_all_recipients()

    line+=f"Number of People Signed up: {len(recipient_list)}\n\n"

    for recipient in recipient_list:
        if recipient.locality in locality_to_num_viewers_dict:
            locality_to_num_viewers_dict[recipient.locality] += 1
        else:
            locality_to_num_viewers_dict[recipient.locality] = 1
    
    line+=f"Number of People viewing Localities (Num Localities Being Tracked : {len(locality_to_num_viewers_dict)}), *N.B. Not shown means 0*:\n"
    for location in locality_to_num_viewers_dict:
        line+=f"{location}: {locality_to_num_viewers_dict[location]}\n"
    line +="\n\n"

    line+="List of all recipients signed up:\n"
    for recipient in recipient_list:
        line+=f"{recipient}\n"
    message.set_content(line)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(environ.get('COVID_EMAIL'), environ.get('COVID_EMAIL_PASSWORD'))
        smtp.send_message(message)