#!/usr/bin/env python
 
import socket
import re
import RPi.GPIO as GPIO
import time
import os
import subprocess

import led
import camera
 
# Standard socket stuff:
host = ''  # do we need socket.gethostname() ?
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)  # don't queue up any requests

# GPIO to Breakout board mappings:
# 11 = 17
# 12 = 18
# 13 = 21 (x)
# 15 = 22
# 16 = 23
# 18 = 24
# 22 = 25

PIN1 = 18
PIN2 = 16

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)
 
# Loop forever, listening for requests:
while True:

	csock, caddr = sock.accept()
	print "Connection from: " + `caddr`
	req = csock.recv(1024)  # get the request, 1kB max
	match = re.match('GET /operate\?key=(led|email|camera|test)&value=(\d+)\sHTTP/1.1', req)
	if match:
		key = match.group(1)
		value = match.group(2)
		print "key: " + key + "\n"
		print "value: " + value + "\n"
		csock.sendall("""
		HTTP/1.1 200 OK
		Content-Type: text/html
		<html><head><title>Success</title></head><body>Boo!</body></html>
		""")
		if key == "camera":
			if value == "1":
				c = camera.Camera("one.jpg")
				c.snap_picture()
			elif value == "2":
	
	        		csock.sendall("""
					HTTP/1.1 200 OK
					Content-Type: text/html
	
					<html>
					<head><title>Jarvis 1.0 - Current Image</title></head>
					<body>
					<img src='http://72.208.62.207:4000/one.jpg'/>
					</body>
					</html>
				""")
	
	    	else:
	        	print "Returning 404"
	
	    	csock.close()
