#!/usr/bin/env python

import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application

class Mailer:
	def __init__(self, x):
		self.x = x
		
	def test(self, email_login, email_password, email_to):
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

		filename='photo.jpg'
		fp=open(filename,'rb')
		att = email.mime.application.MIMEApplication(fp.read(),_subtype="jpg")
		fp.close()
		att.add_header('Content-Disposition','attachment',filename=filename)
		msg.attach(att)

		server.sendmail(email_to,[email_to], msg.as_string())
		server.quit()