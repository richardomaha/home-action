#!/usr/bin/env python

import smtplib
import os

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime.application

import socket
import urllib2
from xml.dom import minidom

class Mailer:
	def __init__(self):
		try:
			result = urllib2.urlopen("http://www.raspiremote.com/api/mailer_settings.xml")
			xmldoc = minidom.parseString(result.read())
			for element in xmldoc.getElementsByTagName('login'):
				self.email_login = element.firstChild.nodeValue
			for element in xmldoc.getElementsByTagName('password'):
				self.email_password = element.firstChild.nodeValue
		except urllib2.URLError, e:
			print("problem")
			#handleError(e)

	def send_email(self, email_to):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()

		#Next, log in to the server
		server.login(self.email_login, self.email_password)

		# Create a text/plain message
		msg = email.mime.Multipart.MIMEMultipart()
		msg['Subject'] = 'intruder alert'
		msg['From'] = self.email_login
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