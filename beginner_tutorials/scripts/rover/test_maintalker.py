#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

callback_received = False
callback_message = ""

def callback(data):
    print("Entered callback function")
    callback_message = data.data
    callback_received = True
    print("Left callback function")
    

def talker():
    #Initialize the publishing channel
    pub = rospy.Publisher('main_publisher', String, queue_size=10)

    #Initialize the subscribing channel
    rospy.Subscriber('main_response', String, callback)

    #Initialize the main node
    rospy.init_node('main', anonymous=True)

    #Set the default rate
    rate = rospy.Rate(10) # 10hz

    #Publish a message
    pub.publish("Hello world")
    print("Published the message")

    #Wait for the call back to be received
    print("Waiting for a reponse")
    #while not callback_received:
    #   rate.sleep()

    #print("Received response")

    #rospy.loginfo(rospy.get_caller_id() + 'I Got Back %s', callback_message)
    #Run until forced to shutdown
    rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
