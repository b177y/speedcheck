# <img src="app/static/speedcheck.ico" width="30"> Speedcheck

## About
This project collects and graphs Internet speed history over time. It uses speedtest-cli to get the data and matplotlib to graph it. This can then be viewed from a very simple web interface (localhost:80)

## Installing
```
git clone https://github.com/billyb1234/speedcheck
cd speedcheck
chmod +x setup.sh
sudo ./setup.sh
```
N.B. setup.sh not finished yet!!

## Alerts
Speedcheck can be configured to send you SMS messages and emails if internet speeds drop below certain thresholds.
To enable these features, navigate to ip:port/settings

### Email
*send_email* is the email address for sending email alerts from.
*send_email_password* is the password for this email account.
*send_email_server* is the server for this email account. E.g. for gmail the server is "smtp.gmail.com"
*send_email_port* is the port of the server for the email account. E.g. for gmail the server is 465.
*receiving_email* is the email to send the alert to (this could be the same as the send_email if you want to send the alerts to yourself.)
*default_subject* is the subject line of the email alert.

### SMS
*twilio_number* is the phone number of your twilio account to send SMS alerts from.
*twilio_API_key* is your api key for your twilio account.
*twilio_SID* is the SID for your twilio account.
*receiving_number* is the phone number you want alerts to be sent to.

### threshold
If the recorded ping is greater than *ping* you will be alerted. If *ping* is 0, alerts will be disabled for ping.
If the recorded download speed is less than *download* you will be alerted. If *download* is 0, alerts will be disabled for download.
If the recorded upload speed is less than *upload* you will be alerted. If *upload* is 0, alerts will be disabled for upload.
