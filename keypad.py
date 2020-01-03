#!/user/bin/env python

import serial
#import RPi.GPIO as GPIO
import time
import json

import display
import audio

#baud_rate = 115200
baud_rate = 9600
ser=serial.Serial("/dev/ttyUSB0", baud_rate)
ser.setDTR(False)
time.sleep(1)
ser.flushInput()
ser.setDTR(True)

with open('interaction.json') as json_file:
    data = json.load(json_file)
    
display.clear()

try:
    while True:
		#if ser.inWaiting() > 0:
		
		keypress = ser.readline().strip()
		print(keypress)
		print('\n')
		try:
			int(keypress)
		except ValueError:
			continue
		print('Key: ' + str(keypress))
		
		try:
			toprint = data[keypress]['displaytext']
			display.display(toprint)
			audio.play(data[keypress]['soundfile'])
		except KeyError:
			pass
			
except KeyboardInterrupt:
    ser.close()
