from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
import json
from pymongo import MongoClient

client = MongoClient()
db = client['speedcheck']
collection = db['config']

if collection.find().count() == 0:
    config = {
            "UseEmail" : 0,
            "UseSMS" : 0,
            "EmailConfig" : {
                "send_email" : "",
                "send_email_password" : "",
                "send_email_server" : "",
                "send_email_port" : "",
                "receiving_email" : "",
                "default_subject" : "SpeedTester Alert"
            },
            "SMSConfig" : {
                "twilio_number" : "",
                "twilio_API_key" : "",
                "twilio_SID" : "",
                "receiving_number" : ""
            },
            "threshold" : {
                "ping" : 0,
                "download" : 0,
                "upload" : 0
            }
        }
    collection.insert_one(config)
else:
    config = collection.find_one()

def alert(message):
    if config['UseSMS'] == 1:
        client = Client(config['SMSConfig']['twilio_SID'], config['SMSConfig']['twilio_API_key'])
        try:
            client.messages.create(to=config['SMSConfig']['receiving_number'], 
                           from_=config['SMSConfig']['twilio_number'], 
                           body=message)
            print("Sending SMS: ", message)
        except Exception as error:
            print("Error sending SMS with twilio, please check your number is verified and details are correct")
    if config['UseEmail'] == 1:
        content = MIMEText(message, "plain")
        content['To'] = config['EmailConfig']['receiving_email']
        content['From'] = config['EmailConfig']['send_email']
        content['Subject'] = config['EmailConfig']['default_subject']
        server = smtplib.SMTP_SSL(config['EmailConfig']['send_email_server'], config['EmailConfig']['send_email_port'])
        server.ehlo()
        server.login(config['EmailConfig']['send_email'], config['EmailConfig']['send_email_password'])
        server.sendmail(config['EmailConfig']['send_email'], config['EmailConfig']['receiving_email'], content.as_string())
        server.close()

def check_result(result):
    alert_msg = ""
    #Ping
    if result['ping'] > config['threshold']['ping'] and config['threshold']['ping'] != 0:
        alert_msg += "Ping is at {0} which is slower than the set threshold of {1}.\n\n".format(result['ping'], config['threshold']['ping'])
    # Download
    if result['download'] < config['threshold']['download'] and config['threshold']['download'] != 0:
        alert_msg += "Download is at {0} which is slower than the set threshold of {1}.\n\n".format(result['download'], config['threshold']['download'])
    # Upload
    if result['upload'] < config['threshold']['upload'] and config['threshold']['upload'] != 0:
        alert_msg += "Upload is at {0} which is slower than the set threshold of {1}.\n\n".format(result['upload'], config['threshold']['upload'])
    if alert_msg != "":
        print(alert_msg)
        alert(alert_msg)
        return True
    else:
        return False
