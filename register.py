#!/user/bin/env python3

import serial
#import RPi.GPIO as GPIO
import time
import json
import sys

import display
import audio

print('Python Version: ', sys.version)

_BAUDRATE = 9600
		
class ArduinoComm:
	def __init__(self, baudrate= 115200, address='/dev/ttyUSB0'):
		self.baudrate = baudrate
		self.address = address
		self.s = serial.Serial(self.address, self.baudrate)
		#reset connection
		self.s.setDTR(False)
		time.sleep(1)
		self.s.flushInput()
		self.s.setDTR(True)
		
	def read(self):
		# returns type bytes
		return self.s.readline().strip()
		
	def close(self):
		self.s.close()


class Register:
	def __init__(self):
		self.keypad = ArduinoComm(_BAUDRATE)
		self.lcd1 = display.display()
		self.data = {}
		print('Starting Register')
		
	def load_config(self, filename):
		with open(filename) as json_file:
			self.data = json.load(json_file)
		print('Loaded ', len(self.data.keys()), ' interactions')

	def loop(self):
		try:
			while True:
				keypress = self.keypad.read()
				try:
					keypress = int(keypress)
				except ValueError:
					print("Error, skipping serial data: ", keypress)
					continue

				try:
					toprint = self.data[str(keypress)]['displaytext']
					self.lcd1.display(toprint)
					audio.play(self.data[str(keypress)]['soundfile'])
				except KeyError as err:
					print('Error, no key in dict: ', err)
					
		except KeyboardInterrupt:
			self.keypad.close()

if __name__ == '__main__':
	r = Register()
	r.load_config('./interaction.json')
	r.loop()
