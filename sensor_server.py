#!/usr/bin/env python

from beginner_tutorials.srv import *
import rospy
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 38
ECHO = 40

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(ECHO,GPIO.IN)

time.sleep(0.1)

GPIO.output(TRIG,1)
time.sleep(0.00001)
GPIO.output(TRIG,0)

def handle_sensor(req):
    #print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    print("Req Received: ", req.a)
    if (req.a == 1):
        rate = rospy.Rate(10)
        distance =  100
        while (distance > 20):
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
            
            print((stop - start) * 17000)
            distance =  ((stop - start) * 17000)

            rate.sleep()

        return(0)

def sensor_server():
    rospy.init_node('sensor')
    s = rospy.Service('sensor', SensorServer, handle_sensor)
    print "Ready to start sensors."
    rospy.spin()

if __name__ == "__main__":
    sensor_server()
