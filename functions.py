
import RPi.GPIO as GPIO
import time
import smbus
import time
import math

GPIO.setmode(GPIO.BCM)

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 10
Motor2B = 9
Motor2E = 11

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

motorR = GPIO.PWM(Motor1E, 100)
motorL = GPIO.PWM(Motor2E, 100)

motorL.start(0)
motorR.start(0)


TRIG = 20
ECHO = 21

TRIG2 = 20
ECHO2 = 21


bus = smbus.SMBus(1)
address = 0x1e

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)


def Initialize():    
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.output(TRIG,0)

    GPIO.setup(ECHO,GPIO.IN)

    time.sleep(0.1)

def Cleanup():
    GPIO.cleanup()

def Turn(direction):
    curr_bearing = GetBearing()
    #print("Curr Bearing %f" % curr_bearing)
    if direction == "Left":
        new_bearing = curr_bearing + 90
        #print("New Bearing %f" % new_bearing)
        if new_bearing > 360:
            new_bearing =  new_bearing - 360
            while (curr_bearing) > 10:
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                motorR.ChangeDutyCycle(40)

                motorL.ChangeDutyCycle(0)
                curr_bearing = GetBearing()
        while new_bearing > curr_bearing:
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            motorR.ChangeDutyCycle(40)

            motorL.ChangeDutyCycle(0)
            curr_bearing = GetBearing()
    elif direction == "Right":
        new_bearing = curr_bearing - 90
        #print("New Bearing %f" % new_bearing)
        if new_bearing < 0:
            new_bearing =   360 + new_bearing
            while curr_bearing < 350:
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                motorL.ChangeDutyCycle(40)

                motorR.ChangeDutyCycle(0)
                curr_bearing = GetBearing()
        while new_bearing < curr_bearing:
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            motorL.ChangeDutyCycle(40)

            motorR.ChangeDutyCycle(0)
            curr_bearing = GetBearing()
    elif direction == "around":
        start = time.time()
        while time.time() - start < 1.15:
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor1E,GPIO.HIGH)

            GPIO.output(Motor2E,GPIO.LOW)
            
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def Stop():
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def GetBearing():
    write_byte(0, 0b01111000) # Set to 8 samples @ 15Hz
    write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
    write_byte(2, 0b00000000) # Continuous sampling

    scale = 0.92

    x_out = read_word_2c(3)
    y_out = read_word_2c(7)
    z_out = read_word_2c(5)
    bearing  = math.atan2(y_out, x_out)
    if (bearing < 0):
        bearing += 2 * math.pi
    #print ("Bearing %f" %math.degrees(bearing))
    time.sleep(0.1)
    return math.degrees(bearing)

def AdjustMovement (correct_bearing):
    curr_bearing = GetBearing()
    if (curr_bearing < correct_bearing - 2):
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        motorR.ChangeDutyCycle(95)
        
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        motorL.ChangeDutyCycle(90)

        return 1
    elif (curr_bearing > correct_bearing + 2):
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        motorL.ChangeDutyCycle(100)
        
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        motorR.ChangeDutyCycle(80)

        return 1
    return 0

def MoveForward(bearing, seconds = 0):
    if (seconds == 0):
        if (AdjustMovement(bearing)):
            pass
        else:
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            motorR.ChangeDutyCycle(95)

            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            motorL.ChangeDutyCycle(100)

    else:
        start = time.time()
        while time.time() - start < seconds:
            if (AdjustMovement(bearing)):
                pass
            else:
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                motorR.ChangeDutyCycle(95)
                
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                motorL.ChangeDutyCycle(100)
                time.sleep(0.1)
 #               Stop()
        Stop()

def GetDistance():
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

    #print ((stop - start) * 17000)
    return ((stop - start) * 17000)            

def GetDistance2():
    GPIO.output(TRIG2,1)
    time.sleep(0.00001)
    GPIO.output(TRIG2,0)

    # wait until the pin goes high
    while GPIO.input(ECHO2) == 0:
        pass
    #record the start time
    start = time.time()

    #wait until the pin goes low
    while GPIO.input(ECHO2) == 1:
        pass
    #record the end time
    stop = time.time()

    #print ((stop - start) * 17000)
    return ((stop - start) * 17000)

def FollowtheWall():
    distance = GetDistance()
    if distance <= 30:
        bearing = GetBearing()
        MoveForward(bearing)
    else:
        Stop()
