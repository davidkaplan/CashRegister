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

init_audio()



