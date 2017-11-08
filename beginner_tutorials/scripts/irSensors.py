#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import lib.PiMotor as PiMotor
import time

state = "on"
sensorR = PiMotor.Sensor("IR1", 10)
sensorL = PiMotor.Sensor("IR2", 10)
response_pub = ""

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global state
    global sensorR
    global sensorL
    state = data.data
    if state == "both":
        sensorR.trigger()
        sensorL.trigger()
    rospy.loginfo(rospy.get_caller_id() + " State changed to " + state)

def setup():
    global response_pub
    
    rospy.init_node('irsensors', anonymous=True)
    
    rospy.Subscriber("irsensors", String, callback)
    
    response_pub = rospy.Publisher('response', String, queue_size=10)
    
if __name__ == '__main__':
    setup()
    global state
    global sensorR
    global sensorL
    global response_pub
    while not rospy.is_shutdown():
        if state == "both":
            sensorR.iRCheck()
            sensorL.iRCheck()
            if sensorL.Triggered or sensorR.Triggered:
                response_pub.publish("stop")
                state = "wait"
