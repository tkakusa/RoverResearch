#!/usr/bin/env python
import rospy
from std_msgs.msg import String
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

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if data.data == " ":
        GPIO.output(Motor1E,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.LOW)
    elif data.data == "w":
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)
        p1.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(100)

def mover():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('mover', anonymous=True)

    rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    mover()

