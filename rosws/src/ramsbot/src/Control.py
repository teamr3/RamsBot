import rospy
import std_msgs.msg
import ramsbot.msg
import Constants as constants
from sensor_msgs.msg import Joy

class DriveTeleop
    def __init__(self):
        self.tank_pub = rospy.Publisher("Ramsbot_Control", ramsbot.msg.Output(), queue_size=1)
        self.speed_ratio = 2 #default shooter speed_ratio
    def on_joy_data(self, data):
        #set shooter speed_ratio
        if data.button[constants.Y]:
            if data.axes[costants.DPad_Vertical] == 1: # d-pad up
                self.speed_ratio  = 1 #full speed
            if data.axes[constants.DPad_Horizontal] != 0: #left or right on the d-pad
                self.speed_ratio = 2 #half speed
            if data.axes[costants.DPad_Vertical] == -1: #down on the d-pad
                self.speed_ratio = 4 #quarter speed

        msg = ramsbot.msg.Output()
        msg.left = -data.axes[constants.Left_Stick_Vertical]
        msg.right = -data.axes[constants.Right_Stick_Vertical]
        msg.shooter = 1/self.speed_ratio

        if data.button[constants.Left_Bumper]: # left bumper
            msg.elevator = 1
        elif data.button[constants.Right_Bumper]: # right bumprt
            msg.elevator = -1
        else:
            msg.elevator = 0

        self.tank_pub.publish(msg)

controller = DriveTeleop()
rospy.init_node("Ramsbot_Control")
joy_sub = rospy.Subscriber("joy", Joy, controller.on_joy_data)
rospy.spin()
