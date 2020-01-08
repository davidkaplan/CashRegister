#!/user/bin/env python3

import serial
#import RPi.GPIO as GPIO
import time
import json
import sys

import display
#import audio
import gameplay
import thermal_printer
import solenoid

print('Python Version: ', sys.version)

_BAUDRATE = 9600
_LCD_FRONT_ADDRESS = 0x27
_LCD_BACK_ADDRESS = 0x26
		
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
		self.lcd_front = display.display(address=_LCD_FRONT_ADDRESS)
		self.lcd_back = display.display(address=_LCD_BACK_ADDRESS)
		self.data = {}
		self.printer = thermal_printer.thermal_printer()
		self.drawer = solenoid.solenoid()
		print('Starting Register')
		
	def open_drawer(self):
		self.drawer.open()
		
	def display_front(self, text):
		self.lcd_front.display(text)
		
	def display_back(self, text):
		self.lcd_back.display(text)
		
	#def play_sound(soundfile):
	#	audio.play(soundfile)
		
	def load_config(self, filename):
		with open(filename) as json_file:
			self.data = json.load(json_file)
		print('Loaded ', len(self.data.keys()), ' interactions')
		
	def read_keypad(self):
		keypress = self.keypad.read()
		try:
			keypress = int(keypress)
		except ValueError:
			print("Error, skipping serial data: ", keypress)
			return
		return keypress
		
	def print_receipt(self, fortune, item_desc_pairs, cust_no):
		self.printer.print_header(cust_no)
		self.printer.print_block(fortune)
		for item, desc in item_desc_pairs:
			self.printer.print_item(item)
			self.printer.print_block(desc)
		self.printer.print_footer()
		
	def __del__(self):
		self.keypad.close()

if __name__ == '__main__':
	r = Register()
	r.open_drawer()
	#r.load_config('./interaction.json')
	#r.loop()
