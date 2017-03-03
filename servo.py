import RPi.GPIO as GPIO
import time

delay = .1
#Horizontal range: 10:14:18
#Vertical range: 12:14:16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

pwm = GPIO.PWM(12, 100)
pwm2 = GPIO.PWM(16, 100)

#Start looking upward
pwm.start(12)
pwm2.start(14)
time.sleep(delay)

#Pan downward
for i in range(12, 16):
    pwm.ChangeDutyCycle(i)
    time.sleep(delay)

#Recenter
pwm.ChangeDutyCycle(14)
pwm2.ChangeDutyCycle(14)
time.sleep(delay)

#Start Left
pwm2.ChangeDutyCycle(10)
time.sleep(delay)

#Pan right
for i in range(10, 18):
    pwm2.ChangeDutyCycle(i)
    time.sleep(delay)

#Recenter
pwm.ChangeDutyCycle(14)
pwm2.ChangeDutyCycle(14)
time.sleep(delay)


GPIO.cleanup()
