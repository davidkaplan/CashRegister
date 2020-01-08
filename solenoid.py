#!/user/bin/env python3

import time
import RPi.GPIO as GPIO

_PIN = 21

class solenoid:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(_PIN, GPIO.OUT)
		GPIO.output(_PIN, GPIO.LOW)
		
	def open(self):
		GPIO.output(_PIN, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(_PIN, GPIO.LOW)

	def test(self):
		try:
			while True:
				GPIO.output(_PIN, GPIO.HIGH)
				time.sleep(0.1)
				GPIO.output(_PIN, GPIO.LOW)
				time.sleep(5)			
		except KeyboardInterrupt:
			pass
			
	def __del__(self):
		GPIO.cleanup()
	
if __name__ == '__main__':
	s = solenoid()
	s.open()

