#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import time
import json

"""
state = "off"
timer = 0
response_pub = ""
"""

class TimerClass:
    def __init__(self, inst_count, time):
        rospy.Timer(rospy.Duration(time), this.timercallback, oneshot=True)

    def timercallback(self, event):
        print 'Timer called at ' + str(event.current_real)
        response_pub.publish("stop")

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if parsed_json["inst_count"].isdigit() and parsed_json["time"].isdigit():
        TimerClass(parsed_json["inst_count"], parsed_json["time"])
    """
    global state
    global timer
    global start
    parsed_json = json.loads(data.data)
    state = parsed_json["state"]
    timer = parsed_json["time"]
    start = time.time()
    """

def setup():
    global response_pub
    
    rospy.init_node('timer', anonymous=True)
    
    rospy.Subscriber('timer', String, callback)
    
    response_pub = rospy.Publisher('response', String, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    setup()
    """
    global state
    global timer
    global start
    while not rospy.is_shutdown():
        if state == "on":
            if (time.time() - start) > timer:
                response_pub.publish("stop")
                state = "off"
    """
