from gameplay import *

def disp_front(x):
	print('display front: ' + x)

def disp_back(x):
	print('display back: ' + x)

def play_sound(x):
 	print('play sound: ' + x)

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

def test_count():
	game = gameplay()
	assert(game.get_and_increment_count(reset=True) == 0)
	assert(game.get_and_increment_count() == 1)
	assert(game.get_and_increment_count() == 2)
	print('0\n1\n2')
	print('test_count passed')
	# Reset Again
	game.get_and_increment_count(reset=True)

if __name__ == '__main__':
	print('test_count:')
	test_count()

	print('test ambient display:')
	sequence = [0, 1, 2, 5, 6, 7, 11, 12, 13, 'q']
	amb = ambient(disp_front, disp_back, play_sound, iter(sequence).__next__)
	amb.display_waiting()
	amb.standard_button('standard button')
	amb.start_button()
	amb.finish_button()
	amb.loop()


	print('test transactions')
	sequence = [0, 1, 2, 5, 8, 9, 10, 14, 15, 16, 'q']
	trans = transaction(disp_front, disp_back, play_sound, iter(sequence).__next__)
	trans.numpad_button(1)
	trans.item_button(1)
	trans.start_button()
	trans.finish_button()
	trans.overloaded()
	trans.loop()

