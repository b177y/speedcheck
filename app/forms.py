from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields import DateField
from pymongo import MongoClient

client = MongoClient()
db = client['speedcheck']
collection = db['config']

days = [ (i, i) for i in range(1, 32) ]
months = [(1, "Jan"),(2, "Feb"),(3, "Mar"),(4, "Apr"), (5, "May"), (6, "Jun"), (7, "Jul"), (8, "Aug"), (9, "Sep"), (10, "Oct"), (11, "Nov"), (12, "Dec")]
years = [("2019", "2019"), ("2020", "2020")]
hours = [ (i, i) for i in range(0, 24) ]
minutes = [ (i, i) for i in range(0, 60) ]

class CustomTime(FlaskForm):
    start_day = SelectField("Day", choices=days)
    start_month = SelectField("Month", choices=months)
    start_year = SelectField("Year", choices=years)
    start_hour = SelectField("Hour", choices=hours, default=0)
    start_minute = SelectField("Minute", choices=minutes, default=0)

    end_day = SelectField("Day", choices=days)
    end_month = SelectField("Month", choices=months)
    end_year = SelectField("Year", choices=years)
    end_hour = SelectField("Hour", choices=hours, default=0)
    end_minute = SelectField("Minute", choices=minutes, default=0)
    
    submit = SubmitField("Go")

class ConfigForm(FlaskForm):
    use_email = BooleanField('Use Email')
    send_email = StringField('Sender Email Address')
    send_email_password = PasswordField('Email Password')
    send_email_server = StringField('Email Server Host')
    send_email_port = IntegerField('Email Server Port')
    receiving_email = StringField('Recipient Email Address')
    default_subject = StringField('Default Email Subject')

    use_sms = BooleanField('Use SMS')
    twilio_number = StringField('Twilio Phone Number')
    twilio_API_key = PasswordField('Twilio API Key')
    twilio_SID = PasswordField('Twilio SID')
    recipient_number = StringField('Recipient Phone Number')


    ping = IntegerField('Max Ping')
    download = IntegerField('Min Download')
    upload = IntegerField('Min Upload')

    submit = SubmitField('Update')
    def load(self):
        conf = collection.find_one()
        self.use_email.default = "checked" if conf['UseEmail'] == 1 else ""
        self.use_sms.default = "checked" if conf['UseSMS'] == 1 else ""
        self.send_email.default = conf['EmailConfig']['send_email']
        self.send_email_password.default = conf['EmailConfig']['send_email_password']
        self.send_email_server.default = conf['EmailConfig']['send_email_server']
        self.send_email_port.default = conf['EmailConfig']['send_email_port']
        self.receiving_email.default = conf['EmailConfig']['receiving_email']
        self.default_subject.default = conf['EmailConfig']['default_subject']
        self.twilio_number.default  = conf['SMSConfig']['twilio_number']
        self.twilio_API_key.default  = conf['SMSConfig']['twilio_API_key']
        self.twilio_SID.default  = conf['SMSConfig']['twilio_SID']
        self.recipient_number.default  = conf['SMSConfig']['receiving_number']
        self.ping.default = conf['threshold']['ping']
        self.download.default = conf['threshold']['download']
        self.upload.default = conf['threshold']['upload']
        self.process()
    def update_db(self):
        conf = {}
        origconf = collection.find_one()
        print(type(self.use_email.data))
        conf['UseEmail'] = 1 if self.use_email.data else 0
        conf['UseSMS'] = 1 if self.use_sms.data else 0
        
        conf['EmailConfig'] = {} 
        conf['EmailConfig']['send_email'] = self.send_email.data
        if self.send_email_password.data != '':
            conf['EmailConfig']['send_email_password'] = self.send_email_password.data
        else:
            conf['EmailConfig']['send_email_password'] = origconf['EmailConfig']['send_email_password']
        conf['EmailConfig']['send_email_server'] = self.send_email_server.data
        conf['EmailConfig']['send_email_port'] = self.send_email_port.data
        conf['EmailConfig']['receiving_email'] = self.receiving_email.data
        conf['EmailConfig']['default_subject'] = self.default_subject.data

        conf['SMSConfig'] = {}
        conf['SMSConfig']['twilio_number'] = self.twilio_number.data
        if self.twilio_API_key.data != '':
            conf['SMSConfig']['twilio_API_key'] = self.twilio_API_key.data
        else:
            conf['SMSConfig']['twilio_API_key'] = origconf['SMSConfig']['twilio_API_key']
        if self.twilio_SID.data != '':
            conf['SMSConfig']['twilio_SID'] = self.twilio_SID.data
        else:
            conf['SMSConfig']['twilio_SID'] = origconf['SMSConfig']['twilio_SID']
        conf['SMSConfig']['receiving_number'] = self.recipient_number.data

        conf['threshold'] = {}
        conf['threshold']['ping'] = self.ping.data
        conf['threshold']['download'] = self.download.data
        conf['threshold']['upload'] = self.upload.data
        collection.replace_one({}, conf)
