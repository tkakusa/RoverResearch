#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import json

def messageBroker():
    pub = rospy.Publisher('instruction', String, queue_size=10)
    rospy.init_node('messageBroker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        motor = raw_input('Input the instruction to the motors: ')
        ultrasonic = raw_input('Input the instruction to the ultrasonic: ')
        timer = int(raw_input('Input the instruction to the timer: '))
        json_dict = {
                    'movement': motor,
                    'ultrasonic': ultrasonic,
                    'timer' : {
                                'state': 'on',
                                'time': timer
                              }
                    }
        pub.publish(json.dumps(json_dict))
        rate.sleep()

if __name__ == '__main__':
    try:
        messageBroker()
    except rospy.ROSInterruptException:
        pass
