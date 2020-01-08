import sys, termios, tty, os, time, random
from itertools import cycle

import audio
import data

class gameplay_config:
	AMBIENT_MAX_BUTTONS = 5
	TRANSACTION_MAX_BUTTONS = 4
	START_BUTTON = 3
	FINISH_BUTTON = 4
	EXIT_BUTTON = 'q'
	RECEIPT_COUNT_FILE = 'count.txt'
	NUMPAD_BUTTONS = [0, 1, 2, 5, 6, 7, 11, 12, 13, 17, 18, 19]
	INACTIVITY_WARNING_TIME = 30
	INACTIVITY_TIMEOUT_TIME = 60

class game_mode:
	ambient = 0
	transaction = 1
	finish = 2
	quit = 3



######################################################################################

class _interface(object):
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func):
		self.display_front = display_front_func
		self.display_back = display_back_func
		self.play_sound = play_sound_func
		self.get_input = get_input_func
		self.cycle_waiting_messages = cycle(range(len(data.ambient_waiting_disp)))

	def display_both(self, text):
		self.display_front(text)
		self.display_back(text)

######################################################################################

class ambient(_interface):
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func):
		super().__init__(display_front_func, display_back_func, play_sound_func, get_input_func)
		#self.mode = game_mode.ambient

	def display_waiting(self):
		'''Cycles messages'''
		self.display_both(data.ambient_waiting_disp[next(self.cycle_waiting_messages)])

	def prompt(self):
		self.display_waiting()
		audio_dir = os.path.join('audio', data.ambient_audio_dir_prompts)
		track = os.path.join(audio_dir, random.choice(os.listdir(audio_dir)))
		self.play_sound(track)

	def standard_button(self, key):
		self.display_waiting()
		audio_dir = os.path.join('audio', data.ambient_audio_dir_buttons)
		track = os.path.join(audio_dir, random.choice(os.listdir(audio_dir)))
		self.play_sound(track)

	def start_button(self):
		txt = 'start button'
		self.display_front(txt)
		self.display_back(txt)
		#self.play_sound(txt)

	def finish_button(self):
		txt = 'finish button'
		self.display_front(txt)
		self.display_back(txt)
		#self.play_sound(txt)

	def loop(self):
		#cont = True
		key_count = 0
		self.display_waiting()
		#time0 = time.time()
		while True:
			key = self.get_input()
			if key == gameplay_config.EXIT_BUTTON:
				return game_mode.quit

			if key == gameplay_config.START_BUTTON:
				self.start_button()
				return game_mode.transaction

			if key == gameplay_config.FINISH_BUTTON:
				self.finish_button

			if key_count >= gameplay_config.AMBIENT_MAX_BUTTONS:
				self.prompt()
				key_count = 0
				continue

			# Else assume standard button
			#print(c)
			self.standard_button(key)
			key_count += 1

######################################################################################


class transaction(_interface):
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func):
		super().__init__(display_front_func, display_back_func, play_sound_func, get_input_func)
		#self.shopping_cart = []
		#self.mode = game_mode.transaction

	def numpad_button(self, key):
		print('transaction numpad button')

	def item_button(self, key):
		print('transaction item button')

	def start_button(self):
		print('transaction start button')

	def finish_button(self):
		print('transaction finish button')

	def overloaded(self):
		print('overload')

	def inactivity_warning(self):
		pass

	def inactivity_timeout(self):
		pass

	def empty_checkout(self):
		print('empty')

	def repeat_selection(self):
		print('repeat')

	def loop(self):
		#cont = True
		#key_count = 0
		start_time = time.time()
		shopping_cart = []
		inactivity_warning_issued = False
		while True:
			current_time = time.time()
			key = self.get_input()
			if key == gameplay_config.EXIT_BUTTON:
				return game_mode.quit

			if not inactivity_warning_issued:
				if (current_time - start_time) > gameplay_config.INACTIVITY_WARNING_TIME:
					self.inactivity_warning()
					inactivity_warning_issued = True

			if (current_time - start_time) > gameplay_config.INACTIVITY_TIMEOUT_TIME:
				self.inactivity_timeout()
				return game_mode.ambient

			if key == gameplay_config.START_BUTTON:
				self.start_button()
				start_time = current_time

			if key == gameplay_config.FINISH_BUTTON:
				if len(shopping_cart) > 0:
					self.finish_button()
					return game_mode.ambient
				else:
					self.empty_checkout()

			if len(shopping_cart) > gameplay_config.TRANSACTION_MAX_BUTTONS:
				# DO SOMETHING
				self.overloaded()
				return game_mode.ambient

			if key in gameplay_config.NUMPAD_BUTTONS:
				self.numpad_button(key)
			else:
				if key in shopping_cart:
					self.repeat_selection()
				else:
					self.item_button(key)
					shopping_cart.append(key)
					print(shopping_cart)


######################################################################################


class gameplay:
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func):
		self.mode = game_mode.ambient
		self.receipt_count_file = os.path.join(os.path.realpath('.'), gameplay_config.RECEIPT_COUNT_FILE)
		self.ambient = ambient(display_front_func, display_back_func, play_sound_func, get_input_func)
		self.transaction = transaction(display_front_func, display_back_func, play_sound_func, get_input_func)
		self.print_receipt = print_receipt_func

	def get_and_increment_count(self, reset=False):
		try:
		    with open(self.receipt_count_file,'r+') as fh:
		    	count = fh.read()
		    	#print('read count', count)
		    	count = int(count)+1
		    	fh.seek(0)
		    	#print('write count', str(count))
		    	if reset:
		    		count = 0
		    	fh.write(str(count))
		except FileNotFoundError:
		    with open(self.receipt_count_file,'w') as fh:
		    	fh.write('0')
		return count
		
	def loop(self):
		try:
			while True:
				if self.mode == game_mode.quit:
					break
				if self.mode == game_mode.ambient:
					self.mode = self.ambient.loop()
				if self.mode == game_mode.transaction:
					self.mode = self.transaction.loop()
		except KeyboardInterrupt:
			pass




	





