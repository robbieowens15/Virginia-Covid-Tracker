import os
import imghdr
from datetime import date
import smtplib, ssl
from email.message import EmailMessage

#print(os.environ.get('COVID_EMAIL'))
#print(os.environ.get('COVID_EMAIL_PASSWORD'))

message = EmailMessage()
message['subject'] = "COVID 19 Update"
message['from'] = 'covidvirginia@gmail.com'
message['to'] = 'raowens2001@gmail.com'
message.set_content('This is a test')
html_message = open('HTML/Fairfax-2020-08-04.html').read()
message.add_alternative(html_message, subtype='html')
with open('HTML/images/Fairfax-7daymovingTotal Cases-2020-08-04.jpg','rb') as attach_file:
    image_name = attach_file.name
    image_type = imghdr.what(attach_file.name)
    image_data = attach_file.read()
message.add_attachment(image_data, maintype='image', subtype=image_type, filename='New Cases vs Time Fairfax DATE')
with open('HTML/images/Fairfax-7daymovingHospitalizations-2020-08-04.jpg','rb') as attach_file:
    image_name = attach_file.name
    image_type = imghdr.what(attach_file.name)
    image_data = attach_file.read()
message.add_attachment(image_data, maintype='image', subtype=image_type, filename='New Hospitalizations vs Time Fairfax DATE')
with open('HTML/images/Fairfax-7daymovingDeaths-2020-08-04.jpg','rb') as attach_file:
    image_name = attach_file.name
    image_type = imghdr.what(attach_file.name)
    image_data = attach_file.read()
message.add_attachment(image_data, maintype='image', subtype=image_type, filename='New Deaths vs Time Fairfax DATE')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('covidvirginia@gmail.com','YC\-4[F&CyadTp!7=M:`.(4g*(T*')
    smtp.send_message(message)

