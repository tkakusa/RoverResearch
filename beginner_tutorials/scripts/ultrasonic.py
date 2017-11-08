#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import lib.PiMotor as PiMotor
import time

state = "off"
sensor = ""
response_pub = ""

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global state
    global sensor
    state = data.data
    if state == "on":
        sensor = PiMotor.Sensor("ULTRASONIC",10)
    rospy.loginfo(rospy.get_caller_id() + " State changed to " + state)

def setup():
    global response_pub
    
    rospy.init_node('ultrasonic', anonymous=True)
    
    rospy.Subscriber('ultrasonic', String, callback)
    
    response_pub = rospy.Publisher('response', String, queue_size=10)
    
if __name__ == '__main__':
    setup()
    global state
    global sensor
    global response_pub
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if state == "on":
            if sensor.Triggered:
                response_pub.publish("stop")
                state = "wait"
            else:
                sensor.sonicCheck()
        rate.sleep()
