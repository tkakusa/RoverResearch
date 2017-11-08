#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    rospy.signal_shutdown("testing")

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    pub.publish("Test")
    
'''
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
'''

if __name__ == '__main__':
    try:
        rospy.Subscriber('return', String, callback)
        talker()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
