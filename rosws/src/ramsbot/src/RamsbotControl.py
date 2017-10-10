#!/usr/bin/python

import rospy
import std_msgs.msg
import smbus
import struct

bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x60
DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d

class DriveTeleop:
    def __init__(self):
        self.speed_ratio = 2
        self.left = 0
        self.right = 0
        self.elevator = 0
        self.shooter = 0

    def on_joy_data(self, data):
        if data.axes[7] == 1:
            self.speed_ratio = 1
        if data.axes[6] != 0:
            self.speed_ratio = 2
        if data.axes[7] == -1:
            self.speed_ratio = 3

        self.left = -data.axes[1]*100/self.speed_ratio
        self.right = -data.axes[4]*100/self.speed_ratio
        data = [struct.pack('i',self.left), struct.pack('i',self.right)]

        bus.write_i2c_block_data(DEVICE_ADDRESS, DEVICE_REG_LEDOUT0, data)

controller = DriveTeleop()
rospy.init_node("ramsbot_teleoperation")
joy_sub = rospy.Subscriber("joy", Joy, controller.on_joy_data)
rospy.spin()
