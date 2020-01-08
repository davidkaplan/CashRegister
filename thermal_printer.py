#!/user/bin/env python3

import serial
import textwrap
import time

uart = serial.Serial("/dev/ttyS0", baudrate=19200, timeout=3000)

import adafruit_thermal_printer

class thermal_printer:
	def __init__(self):
		ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
		self.printer = ThermalPrinter(uart, auto_warm_up=False)
		
	def print(self, text):
		self.printer.print(text)
		
	def print_block(self, text):
		WIDTH = 32
		lines = textwrap.wrap(text, WIDTH-4)
		self.print('*'*WIDTH)
		self.print('*' + ' '*(WIDTH-2) + '*')
		for line in lines:
			f = ('* ' + ('{: ^' + str(WIDTH-4) + '}').format(line) + ' *')
			self.print(f)
		self.print('*' + ' '*(WIDTH-2) + '*')
		self.print('*'*WIDTH)
		self.printer.feed(1)
		
	def print_item(self, item_name):
		self.printer.print('{:.<16}{:.>16}'.format(item_name, 'QT 1'))
		self.printer.feed(1)
		
	def print_header(self, customer_number=0):
		self.printer.feed(5)
		self.printer.size = adafruit_thermal_printer.SIZE_LARGE
		self.printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
		self.printer.inverse = True
		self.printer.print(' VAL-U-MART ')
		self.printer.inverse = False
		self.printer.size = adafruit_thermal_printer.SIZE_SMALL
		self.printer.print('...where everything has a price!')
		#printer.feed(2)

		self.printer.print('January 8 - 18, 2020')
		self.printer.feed(1)

		self.printer.print('150 Frank H. Ogawa Plaza')
		self.printer.print('Oakland, CA 94612')
		
		self.printer.feed(1)
		self.printer.print(time.strftime('%a %m/%d/%Y    %I:%M %p'))
		
		self.printer.feed(1)
		self.printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
		self.printer.print('{0}{1:04d}'.format('Customer Number: ', customer_number))
		
		#printer.print('1234567890123456789012345678901234567890')
		#printer.feed(4)
		
		self.printer.feed(1)

	
	def print_footer(self):
		self.printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
		self.printer.size = adafruit_thermal_printer.SIZE_SMALL
		self.printer.bold = True
		self.printer.print('All sales final, no returns.')
		self.printer.bold = False
		self.printer.feed(1)
		self.printer.size = adafruit_thermal_printer.SIZE_MEDIUM
		self.printer.print('Thanks for shopping with us!')
		self.printer.print('Come again soon!')
		self.printer.print_barcode('948372401763', self.printer.UPC_A)
		self.printer.feed(5)


def test():
	printer = thermal_printer().printer
	printer.test_page()
	printer.feed(2)

	# Print a line of text:
	printer.print('Hello world!')

	# Print a bold line of text:
	printer.bold = True
	printer.print('Bold hello world!')
	printer.bold = False

	# Print a normal/thin underline line of text:
	printer.underline = adafruit_thermal_printer.UNDERLINE_THIN
	printer.print('Thin underline!')

	# Print a thick underline line of text:
	printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
	printer.print('Thick underline!')

	# Disable underlines.
	printer.underline = None

	# Print an inverted line.
	printer.inverse = True
	printer.print('Inverse hello world!')
	printer.inverse = False

	# Print an upside down line.
	printer.upside_down = True
	printer.print('Upside down hello!')
	printer.upside_down = False

	# Print a double height line.
	printer.double_height = True
	printer.print('Double height!')
	printer.double_height = False

	# Print a double width line.
	printer.double_width = True
	printer.print('Double width!')
	printer.double_width = False

	# Print a strike-through line.
	printer.strike = True
	printer.print('Strike-through hello!')
	printer.strike = False

	# Print medium size text.
	printer.size = adafruit_thermal_printer.SIZE_MEDIUM
	printer.print('Medium size text!')

	# Print large size text.
	printer.size = adafruit_thermal_printer.SIZE_LARGE
	printer.print('Large size text!')

	# Back to normal / small size text.
	printer.size = adafruit_thermal_printer.SIZE_SMALL

	# Print center justified text.
	printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
	printer.print('Center justified!')

	# Print right justified text.
	printer.justify = adafruit_thermal_printer.JUSTIFY_RIGHT
	printer.print('Right justified!')

	# Back to left justified / normal text.
	printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT

	# Print a UPC barcode.
	printer.print('UPCA barcode:')
	printer.print_barcode('123456789012', printer.UPC_A)

	# Feed a few lines to see everything.
	printer.feed(2)
	
	

if __name__ == '__main__':
	#test()
	some_text = '''Hurray! Equality is here! Splitting financial costs equally makes total sense and is the best way to show that you care about equality. Don't patronize ppl with marginalized identities by picking up more of the costs of things; it makes them feel equal and important to privledged people to pay the same even though their ability to earn (and pay for) things is less due to their identity alone!'''

	p = thermal_printer()
	
	#p.print_header()
	p.print_block(some_text)
	p.print_item('love')
	p.print_footer()
	p.printer.feed(8)
	

	

