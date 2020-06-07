#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Twist

def callback(msg):
    global pub
    pub.publish(msg)

def start():
   global sub
   sub = rospy.Subscriber('/cmd_vel', Twist , callback)
   rospy.init_node('cmd_vel_to_RosAria', anonymous=True)
   rospy.spin()

def start2():
   global pub
   pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=10)

if __name__ == '__main__':
   time.sleep(1)
   start2()
   start()

