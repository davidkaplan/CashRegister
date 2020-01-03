#!/user/bin/env python

import os
import pygame

if pygame.mixer.get_init():
	pygame.mixer.quit()

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

os.system('amixer sset \'PCM\' 100%')

def play(soundfile):
	soundfile = 'audio/' + soundfile
	pygame.mixer.music.load(soundfile)
	pygame.mixer.music.play()
