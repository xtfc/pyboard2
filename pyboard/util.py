import os
import smtplib
from collections import defaultdict
from email.mime.text import MIMEText
from pyboard.app import app

def open_sql(filename):
	with open(os.path.join('sql', filename + '.sql')) as sql:
		return sql.read()

def group(items, key):
	groups = defaultdict(list)
	for item in items:
		groups[item[key]].append(item)
	return groups


def send_email(sender=None, recipients=None, subject='Pyboard', body=None):
	if not sender:
		sender = app.config['EMAIL_FROM']
	if not recipients or not body:
		return

	if type(recipients) in (str, unicode):
		recipients = [recipients]

	message = MIMEText(body, 'html')
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = ', '.join(recipients)

	mail = smtplib.SMTP('localhost')
	mail.sendmail(sender, recipients, message.as_string())
	mail.quit()
