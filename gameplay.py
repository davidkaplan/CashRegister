import sys, termios, tty

EXIT_CHAR = 'e'
AMBIENT_MAX_BUTTONS = 5
GAMEPLAY_MAX_BUTTONS = 4
START_BUTTON = 's'
FINISH_BUTTON = 'f'

def get_input():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def play_sound(soundfile):
	print 'play sound ' + soundfile

def display_front(text):
	print 'display front ' + text

def display_back(text):
	print 'display back ' + text

class game_mode:
	ambient = 0
	gameplay = 1
	finish = 2

class gameplay:

	def __init__(self):
		self.mode = game_mode.ambient

	def loop_ambient(self):
		cont = True
		key_count = 0
		display_front('Hi I\'m Cassie')
		display_back('Press My Buttons')
		while cont:
			c = get_input()
			if c == EXIT_CHAR:
				return 'break'
			print c
			play_sound(c)
			key_count += 1
			print key_count
			if c == START_BUTTON:
				self.mode = game_mode.gameplay
				return
			if key_count >= AMBIENT_MAX_BUTTONS:
				cont = False
				play_sound('press my start button to begin!')
				key_count = 0
				continue

	def loop_gameplay(self):
		cont = True
		key_count = 0
		cart = []
		while cont:
			c = get_input()
			if c == EXIT_CHAR:
				return 'break'
			print c
			display_front(c)
			display_back(c)
			play_sound(c)
			if c == FINISH_BUTTON:
				self.finish(cart)
				self.mode = game_mode.ambient
				return
			cart.append(c)
			print cart
			if len(cart) > GAMEPLAY_MAX_BUTTONS:
				cont = False
				display_front('I\'m tired')
				display_back('I\'m tired')
				play_sound('I\'m tired')
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
	game = gameplay()
	game.main()



