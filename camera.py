#!/usr/bin/env python

import os
import subprocess

class Camera:
	def __init__(self, filename):
		self.filename = filename
		
	def snap_picture(self):
		try:
			os.remove("/var/www/"+self.filename)
		except OSError:
			pass
		try:
			cmd = 'raspistill -o /var/www/' + self.filename + ' -q 50 -w 640 -h 480'
			pid = subprocess.call(cmd, shell=True)
		except KeyboardInterrupt:
			print "\nGoodbye!"