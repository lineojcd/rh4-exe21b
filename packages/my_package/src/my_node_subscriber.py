#!/usr/bin/env python3

import os
import rospy
import rosnode
from duckietown.dtros import DTROS,NodeType
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String
import rosbag
import numpy as np
from cv_bridge import CvBridge
import cv2

class MyNode(DTROS):

    def __init__(self, node_name,bag):
        # initialize the DTROS parent class
        #color = rospy.get_param('~color')
        super(MyNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.pub = rospy.Publisher('/amd64/camera_node_{}/image/compressed'.format(color), CompressedImage, queue_size=10)
        self.sub = rospy.Subscriber('/jcdgo/camera_node/image/compressed', CompressedImage, self.callback)
        #self.sub = rospy.Subscriber('chatter', String, self.callback)
        self.iter = 0

        # create bag files:
        self.bag = bag

    def callback(self, data):
        if data:
            #colorr = rospy.get_param("/my_node_red/color")
            np_arr = np.fromstring(data.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            #rospy.loginfo("I heard {}".format(np.shape(img)))
            #rospy.loginfo("{}".format(ns))

            print("color in call back:", color)
            img2 = add_rectangle(img,color)

            if self.iter %1000 ==0:
                # cv2.imwrite("mounted_volume/testimgdector.png", img2)
                cv2.imwrite("/code/catkin_ws/src/rh4-exe21b/mounted_v/testimgdector.png", img2)
                print("Saved the test dected images", self.iter)
                self.iter +=1
    #     		print("info of this image:")

            self.iter +=1

            compressed_img_msg = br.cv2_to_compressed_imgmsg(img2, dst_format='jpg')
            # self.bag.write('/jcdgo/camera_node/image/compressed', compressed_img_msg)
            # rospy.loginfo("Publishing color detected img msg")

            write2bag(self.bag,compressed_img_msg )
            self.pub.publish(compressed_img_msg)
        else:
            rospy.loginfo("waiting for Publisher")


if __name__ == '__main__':
    # create the node
    ns = rospy.get_namespace()
    color = str(ns[1:-1])
    print("color in main function:", color)
    br = CvBridge()

    def add_rectangle(img, color):
        #  HSV range
        if color == "red":
            lower = np.array([0, 100, 0])
            upper = np.array([5, 255, 255])
        if color == "yellow":
            lower = np.array([20, 100, 100])
            upper = np.array([30, 255, 255])

        # check color in HSV range
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lower, upper)
        res_0 = cv2.bitwise_and(img,img,mask=mask)

        image = res_0
        t = 0.05
        # create binary image
        gray = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(src = gray,
            ksize = (5, 5),
            sigmaX = 0)

        (t, binary) = cv2.threshold(src = blur,
            thresh = t,
            maxval = 255,
            type = cv2.THRESH_BINARY)

        # find contours
        # _, contours, _ = cv2.findContours(image = binary, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE)

        # in newer version of cv2, it  only return 2 stuff instead of 3
        contours, hierarchy = cv2.findContours(image=binary, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(shape = image.shape, dtype = "uint8")

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)

            cv2.rectangle(img = img,
                pt1 = (x, y),
                pt2 = (x + w, y + h),
                color = (0, 255, 0), thickness = 2)
        return img

    #color = rospy.get_param("/my_node_red/color")

    def write2bag(bag_file, write_msg):
        bag_file.write( '/jcdgo/camera_node/image/compressed' ,write_msg )


    # bag = rosbag.Bag('mounted_volume/amod20-rh3-ex-color-xiaoao-song.bag', 'w')
    bag = rosbag.Bag('/code/catkin_ws/src/rh4-exe21b/mounted_v/amod20-rh3-ex-color-xiaoao-song.bag', 'w')
    node = MyNode(node_name='my_subscriber_node', bag=bag)
    # keep spinning
    rospy.spin()