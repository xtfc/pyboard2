import smtplib
from email.mime.text import MIMEText
from pyboard.app import app


def send_email(me = None, you = None, subject = 'Notification', body = None):
	if not me:
		me = app.config['EMAIL_FROM']
	if not you or not body:
		return

	if type(you) is str or type(you) is unicode:
		you = [you]

	message = MIMEText(body, 'html')
	message['Subject'] = subject
	message['From'] = me
	message['To'] = ', '.join(you)

	s = smtplib.SMTP('localhost')
	s.sendmail(me, you, message.as_string())
	s.quit()
