#!/user/bin/env python

import serial
#import RPi.GPIO as GPIO
import time
import json

import display
import audio

_BAUDRATE = 9600

audio.init_audio()
		
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
		return self.s.readline().strip()
		
	def close(self):
		self.s.close()


class Register:
	def __init__(self):
		self.keypad = ArduinoComm(_BAUDRATE)
		self.lcd1 = display.display()
		self.data = {}
		
	def load_config(self, filename):
		with open(filename) as json_file:
			self.data = json.load(json_file)

	def loop(self):
		try:
			while True:
				keypress = self.keypad.read()
				try:
					int(keypress)
				except ValueError:
					print("Error, skipping value:")
					print(keypress)
					continue
				print('Key: ' + str(keypress))
				
				try:
					toprint = self.data[keypress]['displaytext']
					self.lcd1.display(toprint)
					audio.play(self.data[keypress]['soundfile'])
				except KeyError:
					pass
					
		except KeyboardInterrupt:
			self.keypad.close()

if __name__ == '__main__':
	r = Register()
	r.load_config('interaction.json')
	r.loop()
