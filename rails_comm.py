#!/usr/bin/env python

import socket
import urllib2
from xml.dom import minidom

class RailsComm:
	def __init__(self):
		self.url = "http://www.raspiremote.com/api/device_settings?device=%s" % socket.gethostname()
		#self.url = "http://service.e-navigation.net/api/xml/routeMetoc"
		self.save_photos = 1
		self.email_notification = 0
		self.email_to = "richard.92672@gmail.com"
		
	def load_device_settings(self):
		try:
        		result = urllib2.urlopen(self.url)
        		xmldoc = minidom.parse(result)
        		for element in xmldoc.getElementsByTagName('errorCode'):
                		self.save_photos =  element.firstChild.nodeValue
		except urllib2.URLError, e:
        		handleError(e)
