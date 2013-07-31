#!/usr/bin/env python
 
import re
import RPi.GPIO as GPIO
import time
import os
import sys
import subprocess

import mailer
import led
import camera

LED = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)

ledpwm = GPIO.PWM(LED, 100)
ledpwm.start(0)

# TODO: move PIR code to class:
PIR = 23
GPIO.setup(PIR, GPIO.IN) 
Current_State  = 0
Previous_State = 0
print "Waiting for PIR to settle ..."
# Loop until PIR output is 0
while GPIO.input(PIR)==1:
	Current_State  = 0    
print "  Ready"
 
while True:
	
	# TODO: add a way to read from a button to put the program in and out of a loop that puts it on hold.
	

	# Read PIR state
	Current_State = GPIO.input(PIR)
	if Current_State==1 and Previous_State==0:
		print "  Motion detected!"
		GPIO.output(LED, True)
		led.pulsate(LED)
		c = camera.Camera("one.jpg")
		c.snap_picture()
		e = mailer.Mailer(1)
		e.send_email(sys.argv[1], sys.argv[2], sys.argv[3])
		GPIO.output(LED, False)

		Previous_State=1
	elif Current_State==0 and Previous_State==1:

		print "  Ready"
		Previous_State=0
		
	# Wait for 10 milliseconds
	time.sleep(0.01)