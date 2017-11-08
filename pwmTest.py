import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

Motor1A = 12
Motor1B = 16
Motor1E = 18

Motor2A = 37
Motor2B = 35
Motor2E = 33

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

p1 = GPIO.PWM(Motor1A, 50)    
q1 = GPIO.PWM(Motor1B, 50)    
p2 = GPIO.PWM(Motor2A, 50)
q2 = GPIO.PWM(Motor2B, 50)

p1.start(0)
q1.start(0)

p2.start(0)
q2.start(0)

time.sleep(0.1)

def Initialize():
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)

    p1 = GPIO.PWM(Motor1A, 50)
    q1 = GPIO.PWM(Motor1B, 50)

    p2 = GPIO.PWM(Motor2A, 50)
    q2 = GPIO.PWM(Motor2B, 50)

    p1.start(0)
    q1.start(0)

    p2.start(0)
    q2.start(0)

    time.sleep(0.1)

def Stop():
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def MoveForward(seconds = 0):
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2E,GPIO.HIGH)
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(100)
    print("in")
    time.sleep(5)


MoveForward()
#Stop()
GPIO.cleanup()
