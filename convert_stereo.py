import os
import os.path
import subprocess

audio_path = 'audio' 
for root, dirs, files in os.walk(audio_path):
	for file in files:
		if os.path.splitext(file)[1] == '.wav':
			oldfile = os.path.join(root, file)
			print oldfile
			newfile = os.path.join('stereo', root, file)
			new_dir = os.path.dirname(newfile)
			if not os.path.exists(new_dir):
				os.makedirs(new_dir)
			subprocess.call(['ffmpeg', '-y', '-i', oldfile, '-af', 'pan=stereo|c0=c0|c1=c0', newfile])
			print oldfile
			print newfile

