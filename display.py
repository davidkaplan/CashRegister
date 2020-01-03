#!/user/bin/env python

from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)

def display(text):
	lcd.clear()
	lcd.write_string(text)
	
def clear():
	lcd.clear()
