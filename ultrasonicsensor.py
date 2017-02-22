import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 38
ECHO = 40

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(ECHO,GPIO.IN)

time.sleep(0.1)

print ("Starting Measurements")

GPIO.output(TRIG,1)
time.sleep(0.00001)
GPIO.output(TRIG,0)

# wait until the pin goes high
while GPIO.input(ECHO) == 0:
    pass
#record the start time
start = time.time()

#wait until the pin goes low
while GPIO.input(ECHO) == 1:
    pass
#record the end time
stop = time.time()

print ((stop - start) * 17000)

GPIO.cleanup()
