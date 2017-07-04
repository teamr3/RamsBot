#!/usr/bin/python

import rospy
import geometry_msgs.msg
import std_msgs.msg
import rover_drive.msg

import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685(address = 0x41, busnum=2)
pwm.set_pwm_freq(60)

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    pulse_length //= 4096     # 12 bits of resolution
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def on_new_tank(data):
    


rospy.init_node("twist_sender")
subscriber_tank = rospy.Subscriber("/cmd_vel_tank", rover_drive.msg.Tank, on_new_tank, queue_size=15)
rospy.spin()
