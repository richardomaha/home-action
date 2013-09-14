#!/usr/bin/env python

import socket
import urllib2
from xml.dom import minidom

class RailsComm:
	def __init__(self):
		self.url = "http://www.raspiremote.com/api/device_settings.xml?name=%s" % socket.gethostname()
		self.save_photos = 1
		self.email_notification = 0
		self.email_to = "richard.92672@gmail.com"
		
	def load_device_settings(self):
		try:
			result = urllib2.urlopen(self.url)
			xmldoc = minidom.parseString(result.read())
			for element in xmldoc.getElementsByTagName('email-notification'):
				self.email_notification = int(element.firstChild.nodeValue)
			for element in xmldoc.getElementsByTagName('email'):
				self.email_to = element.firstChild.nodeValue
		except urllib2.URLError, e:
			print("problem")
			#handleError(e)
