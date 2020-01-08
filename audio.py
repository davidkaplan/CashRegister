#!/user/bin/env python3

import os
import os.path
import random
import pygame

def init_audio():
	if pygame.mixer.get_init():
		pygame.mixer.quit()
	#pygame.mixer.pre_init(frequency=22050, size=16, channels=2, buffer=2048)
	pygame.mixer.init(frequency=44100)
	os.system('amixer sset \'PCM\' 100%')

def play(soundfile):
	pygame.mixer.music.load(soundfile)
	pygame.mixer.music.play()
	#with open(soundfile, 'r') as fh:
	#	s = pygame.mixer.Sound(soundfile)
	#	s.play()
	print('playing audio', soundfile)
	
def is_busy():
	return pygame.mixer.music.get_busy()

init_audio()

if __name__ == '__main__':
	import time
	a = './audio/05a - Push 1 SFX/push 1 [2020-01-07 222006].wav'
	b = './audio/05b - Push 1 Phrase/Push 1-Norm_01.wav'
	play(a)
	while is_busy():
		time.sleep(0.01)
	play(b)
	time.sleep(5)



