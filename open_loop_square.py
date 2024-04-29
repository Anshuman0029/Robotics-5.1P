#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped, FSMState
from math import radians

class Drive_Square:
    def _init_(self):
        # Initialize global class variables
        self.cmd_msg = Twist2DStamped()

        # Initialize ROS node
        rospy.init_node('drive_square_node', anonymous=True)
        
        # Initialize Pub/Subs
        self.pub = rospy.Publisher('/ansh1gaurish/car_cmd_switch_node/cmd', Twist2DStamped, queue_size=1)
        rospy.Subscriber('/ansh1gaurish/fsm_node/mode', FSMState, self.fsm_callback, queue_size=1)
        
    # Callback for FSM state changes
    def fsm_callback(self, msg):
        rospy.loginfo("State: %s", msg.state)
        if msg.state == "NORMAL_JOYSTICK_CONTROL":
            self.stop_robot()
        elif msg.state == "LANE_FOLLOWING":            
            rospy.sleep(1) # Wait for a sec for the node to be ready
            self.move_robot()
 
    # Sends zero velocities to stop the robot
    def stop_robot(self):
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.0
        self.cmd_msg.omega = 0.0
        self.pub.publish(self.cmd_msg)
 
    # Spin forever but listen to message callbacks
    def run(self):
        rospy.spin() # keeps node from exiting until node has shutdown

    # Robot drives in a square and then stops
    def move_robot(self):
        # Define the side length of the square
        side_length = 0.5  # Adjust as needed
        
        # Move forward
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.5 # straight line velocity
        self.cmd_msg.omega = 0.0
        self.pub.publish(self.cmd_msg)
        rospy.loginfo("Forward!")
        rospy.sleep(side_length) # Move forward for side_length
        
        # Stop
        self.stop_robot()
        rospy.loginfo("Stopped")
        rospy.sleep(1) # Wait for a sec
        
        # Rotate 90 degrees clockwise
        self.cmd_msg.header.stamp = rospy.Time.now()
        self.cmd_msg.v = 0.0
        self.cmd_msg.omega = radians(-90) # Rotate clockwise
        self.pub.publish(self.cmd_msg)
        rospy.loginfo("Rotate clockwise!")
        rospy.sleep(1) # Rotate for 1 second (adjust as needed)
        
        # Stop
        self.stop_robot()
        rospy.loginfo("Stopped")
        rospy.sleep(1) # Wait for a sec

if __name__ == '_main_':
    try:
        duckiebot_movement = Drive_Square()
        duckiebot_movement.run()
    except rospy.ROSInterruptException:
        pass