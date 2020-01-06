#!/user/bin/env python3

import serial
import textwrap
import time

uart = serial.Serial("/dev/ttyS0", baudrate=19200, timeout=3000)

import adafruit_thermal_printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)

printer = ThermalPrinter(uart, auto_warm_up=False)

some_text = '''Hurray! Equality is here! Splitting financial costs equally makes total sense and is the best way to show that you care about equality. Don't patronize ppl with marginalized identities by picking up more of the costs of things; it makes them feel equal and important to privledged people to pay the same even though their ability to earn (and pay for) things is less due to their identity alone!'''

def test():
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
	
	
def format_text():
	WIDTH = 32
	lines = textwrap.wrap(some_text, WIDTH-4)
	printer.print('*'*WIDTH)
	printer.print('*' + ' '*(WIDTH-2) + '*')
	for line in lines:
		f = ('* ' + ('{: ^' + str(WIDTH-4) + '}').format(line) + ' *')
		printer.print(f)
	printer.print('*' + ' '*(WIDTH-2) + '*')
	printer.print('*'*WIDTH)
	

def header():
	printer.feed(1)
	printer.size = adafruit_thermal_printer.SIZE_LARGE
	printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
	printer.inverse = True
	printer.print(' VAL-U-MART ')
	printer.inverse = False
	printer.size = adafruit_thermal_printer.SIZE_SMALL
	printer.print('...where everything has a price!')
	#printer.feed(2)

	printer.print('January 8 - 18, 2020')
	printer.feed(1)

	printer.print('150 Frank H. Ogawa Plaza')
	printer.print('Oakland, CA 94612')
	
	printer.feed(1)
	printer.print(time.strftime('%a %m/%d/%Y    %I:%M %p'))
	
	printer.feed(1)
	printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
	printer.print('{0}{1:04d}'.format('Customer Number: ', 1))
	
	#printer.print('1234567890123456789012345678901234567890')
	#printer.feed(4)
	
	printer.feed(1)
	
def some_items():
	printer.print('{:.<16}{:.>16}'.format('Love', 'QT 1'))
	printer.feed(1)

	format_text()
	printer.feed(1)
	
	printer.print('{:.<16}{:.>16}'.format('Intimacy', 'QT 2'))
	printer.feed(1)

	format_text()
	printer.feed(2)
	

	
if __name__ == '__main__':
	header()
	some_items()

	

