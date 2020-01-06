#!/user/bin/env python3

from RPLCD.i2c import CharLCD

class display:
	def __init__(self, chipset='PCF8574', address=0x27, cols=18, rows=2):
		self.lcd = CharLCD(chipset, address, cols=cols, rows=rows)
		self.clear()

	def display(self, text):
		self.lcd.clear()
		self.lcd.write_string(text)
		
	def clear(self):
		self.lcd.clear()

if __name__ == '__main__':
	d1 = display(address=0x27)
	d1.display('oo first display')

	d2 = display(address=0x26)
	d2.display('aa second display')
	
