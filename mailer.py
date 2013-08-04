#!/usr/bin/env python

import smtplib
import os

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application

class Mailer:
	def __init__(self):
		self.x = "test"
		
	def send_email(self, email_login, email_password, email_to):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()

		#Next, log in to the server
		server.login(email_login, email_password)

		# Create a text/plain message
		msg = email.mime.Multipart.MIMEMultipart()
		msg['Subject'] = 'intruder alert'
		msg['From'] = email_login
		msg['To'] = email_to

		# The main body is just another attachment
		body = email.mime.Text.MIMEText("""Alert - someone is at your back door.""")
		msg.attach(body)

		# Get the most recent photo:
		photodir='/var/www/photos'
		files = sorted([ f for f in os.listdir(photodir)])
		f = files[-1]
		
		fp=open(photodir + "/" + f,'rb')
		att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
		fp.close()
		att.add_header('Content-Disposition','attachment',filename=f)
		msg.attach(att)

		server.sendmail(email_to,[email_to], msg.as_string())
		server.quit()