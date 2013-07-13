#!/usr/bin/env python
 
import socket
import re
import RPi.GPIO as GPIO
import time
 
# Standard socket stuff:
host = ''  # do we need socket.gethostname() ?
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)  # don't queue up any requests

PIN1 = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIN1, GPIO.OUT)
 
# Loop forever, listening for requests:
while True:
    csock, caddr = sock.accept()
    print "Connection from: " + `caddr`
    req = csock.recv(1024)  # get the request, 1kB max

    a = req.find("/move")
    print a

    match = re.match('GET /operate\?key=(led|camera)&value=(\d+)\sHTTP/1.1', req)
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
	
	GPIO.output(PIN1, True)
	time.sleep(1.5)
	GPIO.output(PIN1, False)
    else:
        print "Returning 404"

    csock.close()
