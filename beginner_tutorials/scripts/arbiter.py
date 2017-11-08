#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import json

movement_pub = ""
ultrasonic_pub = ""
timer_pub = ""


def instruction_callback(data):
    global movement_pub
    global ultrasonic_pub
    global timer_pub
    json_string = data.data
    print("Received: " + json_string)
    json_form = json.loads(json_string)
    movement_pub.publish(json_form["movement"])
    ultrasonic_pub.publish(json_form["ultrasonic"])
    timer_pub.publish(json.dumps(json_form["timer"]))

def response_callback(data):
    global movement_pub
    global ultrasonic_pub
    global timer_pub
    movement_pub.publish("s")
    ultrasonic_pub.publish("wait")
    timer_pub.publish('{"state": "off", "time": 0}')

def setup():
    global movement_pub
    global ultrasonic_pub
    global timer_pub
    rospy.init_node('arbiter', anonymous=True)
    
    movement_pub = rospy.Publisher('movement', String, queue_size=10)
    ultrasonic_pub = rospy.Publisher('ultrasonic', String, queue_size=10)
    timer_pub = rospy.Publisher('timer', String, queue_size=10)
    rospy.Subscriber("instruction", String, instruction_callback)
    rospy.Subscriber("response", String, response_callback)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        setup()
    except rospy.ROSInterruptException:
        pass
