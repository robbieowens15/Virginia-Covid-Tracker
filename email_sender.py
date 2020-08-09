import os
import imghdr
from datetime import date
import smtplib, ssl
from email.message import EmailMessage

import process_data as pd

#print(os.environ.get('COVID_EMAIL'))
#print(os.environ.get('COVID_EMAIL_PASSWORD'))
date = date.today().isoformat()

def send_mail(locality):
    message = EmailMessage()
    message['subject'] = "COVID 19 Update"
    message['from'] = 'covidvirginia@gmail.com'
    message['to'] = 'raowens2001@gmail.com'
    message.set_content('Enable HTML to view this message')
    html_message = open(f'HTML/{locality.name}-{date}.html').read()
    message.add_alternative(html_message, subtype='html')
    with open(f'HTML/images/{locality.name}-7daymovingTotal Cases-{date}.jpg','rb') as attach_file:
        image_name = attach_file.name
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'New Cases vs Time Fairfax {date}')
    with open(f'HTML/images/{locality.name}-7daymovingHospitalizations-{date}.jpg','rb') as attach_file:
        image_name = attach_file.name
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'New Hospitalizations vs Time Fairfax {date}')
    with open(f'HTML/images/{locality.name}-7daymovingDeaths-{date}.jpg','rb') as attach_file:
        image_name = attach_file.name
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'New Deaths vs Time Fairfax {date}')

    with open(f'HTML/images/{locality.name}-cumvstimeTotal Cases-{date}.jpg','rb') as attach_file:
        image_name = attach_file.name
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'Total Cases vs Time Fairfax {date}')

    with open(f'HTML/images/{locality.name}-cumvstimeHospitalizations-{date}.jpg','rb') as attach_file:
        image_name = attach_file.name
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'Total Hospitalizations vs Time Fairfax {date}')

    with open(f'HTML/images/{locality.name}-cumvstimeDeaths-{date}.jpg','rb') as attach_file:
        image_name = attach_file.name
        image_type = imghdr.what(attach_file.name)
        image_data = attach_file.read()
    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=f'Total Deaths vs Time Fairfax {date}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('covidvirginia@gmail.com','YC\-4[F&CyadTp!7=M:`.(4g*(T*')
        smtp.send_message(message)

send_mail(pd.tracking_loalities[0])