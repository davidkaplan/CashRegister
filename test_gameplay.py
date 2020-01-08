from gameplay import *

def disp_front(x):
	print('display front: ' + x)

def disp_back(x):
	print('display back: ' + x)

def play_sound(x):
 	print('play sound: ' + x)

def print_receipt(fortune, item_desc_pairs, cust_no):
	print('BEGIN RECEIPT')
	print('Fortune:')
	print(fortune)
	for item, desc in item_desc_pairs:
		print('Item:')
		print(item)
		print('Description')
		print(desc)

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
	sequence = [0, 1, 2, 5, 6, 7, 11, 12, 13, 'q']
	game = gameplay(disp_front, disp_back, play_sound, iter(sequence).__next__, print_receipt)
	assert(game.get_and_increment_count(reset=True) == 0)
	assert(game.get_and_increment_count() == 1)
	assert(game.get_and_increment_count() == 2)
	print('0\n1\n2')
	print('test_count passed')
	# Reset Again
	game.get_and_increment_count(reset=True)

def test_ambient():
	print('test ambient display:')
	sequence = [0, 1, 2, 5, 6, 7, 11, 12, 13, 'q']
	amb = ambient(disp_front, disp_back, play_sound, iter(sequence).__next__)
	amb.display_waiting()
	amb.standard_button('standard button')
	amb.start_button()
	amb.finish_button()
	amb.loop()


def test_transaction():
	print('test transactions')
	sequence = [0, 1, 2, 5, 8, 9, 10, 14, 15, 16, 'q']
	trans = transaction(disp_front, disp_back, play_sound, iter(sequence).__next__)
	trans.numpad_button(1)
	trans.item_button(1)
	trans.start_button()
	trans.finish_button()
	trans.overloaded()
	trans.loop()

def test_transaction():
	sequence = [3, 8, 9, 4, 'q']
	game = gameplay(disp_front, disp_back, play_sound, iter(sequence).__next__, print_receipt)
	game.loop()

def test_overload():
	sequence = [3, 8, 9, 10, 14, 15, 16, 4, 'q']
	game = gameplay(disp_front, disp_back, play_sound, iter(sequence).__next__, print_receipt)
	game.loop()

def test_empty():
	sequence = [3, 4, 'q']
	game = gameplay(disp_front, disp_back, play_sound, iter(sequence).__next__, print_receipt)
	game.loop()

def test_repeat():
	sequence = [3, 8, 8, 4, 'q']
	game = gameplay(disp_front, disp_back, play_sound, iter(sequence).__next__, print_receipt)
	game.loop()


if __name__ == '__main__':
	test_ambient()
	#test_transaction()
	#test_overload()
	#test_empty()
	#test_overload()
	#test_repeat()






