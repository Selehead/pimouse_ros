#!/usr/bin/env python
import sys, rospy
from pimouse_ros.msg import lightsensorvalues

if __name__ == '__main__':
    devfile = '/dev/rtlightsensor0'
    rospy.init_node('lightsensors')
    pub = rospy.Publisher('lightsensors',lightsensorvalues, queue_size=1)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            with open(devfile,'r') as f:
                data = f.readline().split()
                data = [ int(e) for e in data ]
                d = lightsensorvalues()
                d.right_forward = data[0]
                d.right_side = data[1]
                d.left_side = data[2]
                d.left_forward = data[3]
                d.sum_all = sum(data)
                d.sum_forward = data[0] + data[3]
                pub.publish(d)
        except IOError:
            rospy.logerr("cannot write to " + devfile)

        rate.sleep()
