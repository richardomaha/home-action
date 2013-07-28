import time
import RPi.GPIO as GPIO

def on(pin, length):
	GPIO.output(pin, True)
	time.sleep(length)
	GPIO.output(pin, False)
	
def pulsate(pin):
	for i in range(0, 50):
		GPIO.output(pin, True)
		time.sleep(0.05)
		GPIO.output(pin, False)
		time.sleep(0.05)