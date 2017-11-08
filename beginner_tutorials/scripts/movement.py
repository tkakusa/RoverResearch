#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import lib.PiMotor as PiMotor
import time

state = "stop"

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global state
    if data.data == "f":
        state = "forward"
    elif data.data == "l":
        state = "left"
    elif data.data == "r":
        state = "right"
    elif data.data == "s":
        state = "stop"
    rospy.loginfo(rospy.get_caller_id() + " State changed to " + state)

def setup():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('mover', anonymous=True)

    rospy.Subscriber("movement", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    setup()
    global state
    motorR = PiMotor.Motor("MOTOR1", 2)
    motorL = PiMotor.Motor("MOTOR2", 2)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        if state == "stop":
            print("Entered state stop")
            motorR.stop()
            motorL.stop()
            state = "wait"
        elif state == "forward":
            print("Entered state forward")
            motorR.forward(50)
            motorL.forward(50)
            state = "wait"
        elif state == "left":
            print("Entered state left")
            motorR.forward(50)
            motorL.stop()
            state = "wait"
        elif state == "right":
            print("Entered state right")
            motorR.stop()
            motorL.forward(50)
            state = "wait"
        rate.sleep()
    print ("Exited")
