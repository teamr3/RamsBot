#!/usr/bin/python

import rospy
import geometry_msgs.msg
import std_msgs.msg
import ramsbot.msg
import Adafruit_PCA9685
import Constans as constants

pwm = Adafruit_PCA9685.PCA9685(address = 0x41, busnum=2)
pwm.set_pwm_freq(60)
msg = ramsbot.msg.Output()

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    pulse_length //= 4096     # 12 bits of resolution
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def on_new_input():
    set_servo_pulse(constants.Left_Drive_Motor, msg.left)
    set_servo_pulse(constants.Right_Drive_Motor, msg.right)
    set_servo_pulse(constants.Elevator_Motor, msg.elevator)
    set_servo_pulse(constants.Shooter_Motor, msg.shooter)

rospy.init_node("Ramsbot_Drive")
Subscriber_Drive = rospy.Subscriber("/Drive", ramsbot.msg,Output, on_new_input, queue_size = 1)
