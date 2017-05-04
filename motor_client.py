#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *

def motor_server(val):
    rospy.wait_for_service('motor')
    try:
        motor = rospy.ServiceProxy('motor', MotorServer)
        resp1 = motor(val)
        return resp1.sum
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def sensor_server(val):
    rospy.wait_for_service('sensor')
    try:
        sensor = rospy.ServiceProxy('sensor', SensorServer)
        resp1 = sensor(val)
        return resp1.sum
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        val1 = int(sys.argv[1])
        val2 = int(sys.argv[2])
    else:
        print usage()
        sys.exit(1)
    print "Requesting %s"%(val1)
    motor_response = motor_server(val1)
    sensor_response = sensor_server(val2)
    motor_server(0)
    #print "%s + %s = %s"%(x, y, add_two_ints_client(x, y))
