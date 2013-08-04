#!/usr/bin/env python

import os
import subprocess
import time

class Camera:
	def __init__(self):
		self.photo_dir = "/var/www/photos/"
		
	def snap_picture(self):
		try:
			filename = str(time.time())+'.jpg'
			cmd = 'raspistill -o ' + self.photo_dir + filename + ' -q 50 -w 640 -h 480'
			pid = subprocess.call(cmd, shell=True)
			return self.photo_dir + filename
		except KeyboardInterrupt:
			print "\nGoodbye!"