#!/usr/bin/env python
 
import socket
import re
import RPi.GPIO as GPIO
import time
import os
import subprocess

import led
import mailer
 
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

PIN1 = 12
PIN2 = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)

led2 = GPIO.PWM(PIN2, 100)

led2.start(0)
 
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

			<html>
			<head>
			<title>Success</title>
			</head>
			<body>
			Boo!
			</body>
			</html>
		""")
		if key == "led":
			if value == "1":
				led.on(PIN1, 2)
			elif value == "2":
				led.pulsate(PIN1)
		elif key == "email":
			e = mailer.Mailer(1)
			e.test()
		elif key == "camera":
			if value == "1":
				try:
					os.remove("/var/www/one.jpg")
				except OSError:
					pass
				try:
					cmd = 'raspistill -o /var/www/one.jpg -q 50 -w 640 -h 480'
					pid = subprocess.call(cmd, shell=True)
				except KeyboardInterrupt:
					print "\nGoodbye!"
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
