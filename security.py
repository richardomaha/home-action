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
import rails_comm

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
rc = rails_comm.RailsComm()

photo_time = 0

while True:
	
	# Read PIR state
	Current_State = GPIO.input(PIR)
	if Current_State==1 and Previous_State==0:
		seconds_passed = time.time() - photo_time
		if seconds_passed >= 600:
			photo_time = time.time()

			GPIO.output(LED, True)
			filename = c.snap_picture()	

			rc.load_device_settings()
			
			if (rc.email_notification==1):
				m.send_email(rc.email_to)

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
