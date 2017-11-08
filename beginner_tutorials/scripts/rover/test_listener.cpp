#include "ros/ros.h"
#include "std_msgs/String.h"

#include <iostream>
#include <stdio>

bool callback_received = 0;
string callback_message = "";
void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
    callback message = msg->data.c_str();
    callback_received = 1;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "listener");

    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe("main_publisher", 1000, chatterCallback)

    std::cout << "Waiting" << std::endl;

    while (!callback_received) {
        ros::spinOnce();
    }

    std::cout << "Done" <<  std::endl;
}
