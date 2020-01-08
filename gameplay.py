import sys, termios, tty

class gameplay_config:
	AMBIENT_MAX_BUTTONS = 5
	GAMEPLAY_MAX_BUTTONS = 4
	START_BUTTON = 3
	FINISH_BUTTON = 4
	EXIT_BUTTON = 'q'

class game_mode:
	ambient = 0
	gameplay = 1
	finish = 2

class gameplay:

	def __init__(self):
		self.mode = game_mode.ambient

	def play_sound(self, soundfile):
		print('Play sound ' + soundfile)

	def display_front(self, text):
		print('Display front: ' + text)

	def display_back(self, text):
		print('Display back: ' + text)

	def read_input_buffer(self):
		return None

	def loop_ambient(self):
		cont = True
		key_count = 0
		self.display_front('Hi I\'m Cassie')
		self.display_back('Press My Buttons')
		while cont:
			c = self.read_input_buffer()
			if c == gameplay_config.EXIT_BUTTON:
				return 'break'
			print(c)
			self.play_sound(str(c))
			key_count += 1
			print(key_count)
			if c == gameplay_config.START_BUTTON:
				self.mode = game_mode.gameplay
				return
			if key_count >= gameplay_config.AMBIENT_MAX_BUTTONS:
				cont = False
				self.play_sound('press my start button to begin!')
				key_count = 0
				continue

	def loop_gameplay(self):
		cont = True
		key_count = 0
		cart = []
		while cont:
			c = self.read_input_buffer()
			if c ==gameplay_config.EXIT_BUTTON:
				return 'break'
			print(c)
			self.display_front(str(c))
			self.display_back(str(c))
			self.play_sound(str(c))
			if c == gameplay_config.FINISH_BUTTON:
				self.finish(cart)
				self.mode = game_mode.ambient
				return
			cart.append(c)
			print(cart)
			if len(cart) > gameplay_config.GAMEPLAY_MAX_BUTTONS:
				cont = False
				self.display_front('I\'m tired')
				self.display_back('I\'m tired')
				self.play_sound('I\'m tired')
				# Wait
				self.mode = game_mode.ambient
				return	

	def finish(self, cart):
		print('printing receipt for items:')
		print(cart)
		# wait


	def main(self):
		while True:
			if self.mode == game_mode.ambient:
				ret = self.loop_ambient()
				if ret == 'break':
					break
			if self.mode == game_mode.gameplay:
				ret = self.loop_gameplay()
				if ret == 'break':
					break


if __name__ == '__main__':

	def get_input():
	    fd = sys.stdin.fileno()
	    old_settings = termios.tcgetattr(fd)
	    try:
	        tty.setraw(sys.stdin.fileno())
	        ch = sys.stdin.read(1)
	 
	    finally:
	        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	    try:
	    	ch = int(ch)
	    except ValueError:
	    	pass
	    return ch

	game = gameplay()
	game.read_input_buffer = get_input
	game.main()



