#!/usr/bin/env python
 
import re
import RPi.GPIO as GPIO
import time
import os
import os.path
import sys
import subprocess

import mailer
import led
import camera

LED = 4
LED2 = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

# ledpwm = GPIO.PWM(LED, 100)
# ledpwm.start(0)

# TODO: move PIR code to class:
PIR = 18
GPIO.setup(PIR, GPIO.IN) 
Current_State  = 0
Previous_State = 0
print "Waiting for PIR to settle ..."
# Loop until PIR output is 0
while GPIO.input(PIR)==1:
	Current_State  = 0    
print "  Ready"
 
c = camera.Camera()
m = mailer.Mailer()

while True:
	
	# Read PIR state
	Current_State = GPIO.input(PIR)
	if Current_State==1 and Previous_State==0:
		print "  Motion detected!"
		GPIO.output(LED, True)
		#GPIO.output(LED2, True)
		#led.pulsate(LED)		
		filename = c.snap_picture()	
		print filename
		if os.path.exists("/home/pi/python/home-action/config/email-notification.1"):
			print "sending email"
			m.send_email(sys.argv[1], sys.argv[2], sys.argv[3])
		GPIO.output(LED, False)
		GPIO.output(LED2, True)
		time.sleep(2)
		GPIO.output(LED2, False)
		time.sleep(20)
		Previous_State=1
	elif Current_State==0 and Previous_State==1:
		print "  Ready"
		Previous_State=0
		
	# Wait for 10 milliseconds
	time.sleep(0.01)
