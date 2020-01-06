#!/user/bin/env python3

import time
import RPi.GPIO as GPIO

solenoid_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(solenoid_pin, GPIO.OUT)

GPIO.output(solenoid_pin, GPIO.HIGH)

time.sleep(0.1)

GPIO.output(solenoid_pin, GPIO.LOW)

GPIO.cleanup()

