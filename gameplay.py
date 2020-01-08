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
	OVERLOAD_SLEEP_TIME = 15

class game_mode:
	ambient = 0
	transaction = 1
	finish = 2
	quit = 3



######################################################################################

class _interface(object):
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func):
		self.display_front = display_front_func
		self.display_back = display_back_func
		self.play_sound = play_sound_func
		self.get_input = get_input_func
		self.print_receipt = print_receipt_func
		self.open_drawer = open_drawer_func

	def display_both(self, text):
		self.display_front(text)
		self.display_back(text)
		
	def _play_random_audio(self, directory):
		audio_dir = os.path.join('audio', directory)
		track = os.path.join(audio_dir, random.choice(os.listdir(audio_dir)))
		self.play_sound(track)
		
	def _play_audio_sequence(self, directories, wait_to_start=False):
		first = not wait_to_start
		for d in directories:
			if not first:
				while audio.is_busy():
					time.sleep(0.01)
			first = False
			self._play_random_audio(d)

######################################################################################

class ambient(_interface):
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func):
		super().__init__(display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func)
		self.cycle_waiting_messages = cycle(data.ambient_waiting_disp)
		self.ambient_checkout_messages = cycle(data.ambient_checkout_disp)

	def display_waiting(self):
		'''Cycles messages'''
		self.display_both(next(self.cycle_waiting_messages))

	def prompt(self):
		self.display_waiting()
		self._play_random_audio(data.ambient_audio_dir_prompts)

	def standard_button(self, key):
		self.display_waiting()
		self._play_random_audio(data.ambient_audio_dir_buttons)

	def start_button(self):
		self.display_waiting()
		#self._play_random_audio(data.start_transaction_audio)

	def finish_button(self):
		self.display_both(next(self.ambient_checkout_messages))

	def loop(self):
		key_count = 0
		self.display_waiting()
		#time0 = time.time()
		while True:
			key = self.get_input()
			print(key)
			if key == gameplay_config.EXIT_BUTTON:
				return game_mode.quit

			if key == gameplay_config.START_BUTTON:
				self.start_button()
				return game_mode.transaction

			if key == gameplay_config.FINISH_BUTTON:
				self.finish_button()
				continue

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
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func):
		super().__init__(display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func)
		#self.shopping_cart = []
		#self.mode = game_mode.transaction
		self.overload_timeout = False
		self.overload_start_time = time.time()
		self.warning_timer = False
		self.warning_start_time = time.time()

	def numpad_button(self, key):
		self._play_random_audio(data.ambient_audio_dir_buttons)
		print('transaction numpad button')

	def item_button(self, key, num):
		print('transaction item button')
		if num == 1:
			self._play_audio_sequence([data.transaction_1_sfx, data.transaction_1_phrase])
		if num == 2:
			self._play_audio_sequence([data.transaction_2_sfx, data.transaction_2_phrase])
		if num == 3:
			self._play_audio_sequence([data.transaction_3_sfx, data.transaction_3_phrase])
		if num == 4:
			self._play_audio_sequence([data.transaction_4_sfx, data.transaction_4_phrase])


	def start_button(self):
		self._play_audio_sequence([data.transaction_empty_checkout_sfx, data.transaction_empty_checkout_phrase])
		print('transaction start button')

	def finish_button(self):
		self._play_audio_sequence([data.checkout_1, data.checkout_2, data.checkout_3, data.checkout_4])
		# wait for sound to finish before opening drawer
		while audio.is_busy():
			time.sleep(0.1)
		self.open_drawer()
		self._play_audio_sequence([data.checkout_drawer_out_sfx, data.checkout_drawer_out_phrase, data.checkout_finale])
	
		# print receipt
		self._play_audio_sequence([data.checkout_farewell, data.transaction_outro_song], wait_to_start=True)
		print('transaction finish button')

	def overloaded(self):
		self._play_audio_sequence([data.transaction_overload_sfx, data.transaction_overload_phrase])
		self.overload_timeout = True
		self.overload_start_time = time.time()
		print('overload')

	def inactivity_warning(self):
		self._play_audio_sequence([data.transaction_inactivity_warning_sfx, data.transaction_inactivity_warning_phrase])

	def inactivity_timeout(self):
		self._play_audio_sequence([data.transaction_timeout_sfx, data.transaction_timeout_phrase])

	def empty_checkout(self):
		self._play_audio_sequence([data.transaction_empty_checkout_sfx, data.transaction_empty_checkout_phrase])
		print('empty')

	def repeat_selection(self):
		self._play_audio_sequence([data.transaction_repeat_sfx, data.transaction_repeat_phrase])
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
			
			if self.overload_timeout:
				if (current_time - self.overload_start_time) < gameplay_config.OVERLOAD_SLEEP_TIME:
					time.sleep(0.1)
					continue
				else:
					self.overload_timeout = False
					return game_mode.ambient
					
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
				continue

			if key == gameplay_config.FINISH_BUTTON:
				if len(shopping_cart) > 0:
					self.finish_button()
					return game_mode.ambient
				else:
					self.empty_checkout()
				continue

			if len(shopping_cart) >= gameplay_config.TRANSACTION_MAX_BUTTONS:
				# DO SOMETHING
				self.overloaded()
				continue

			if key in gameplay_config.NUMPAD_BUTTONS:
				self.numpad_button(key)
			else:
				if key in shopping_cart:
					self.repeat_selection()
				else:
					shopping_cart.append(key)
					self.item_button(key, len(shopping_cart))
					print(shopping_cart)


######################################################################################


class gameplay:
	def __init__(self, display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func):
		self.mode = game_mode.ambient
		self.receipt_count_file = os.path.join(os.path.realpath('.'), gameplay_config.RECEIPT_COUNT_FILE)
		self.ambient = ambient(display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func)
		self.transaction = transaction(display_front_func, display_back_func, play_sound_func, get_input_func, print_receipt_func, open_drawer_func)

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




	





