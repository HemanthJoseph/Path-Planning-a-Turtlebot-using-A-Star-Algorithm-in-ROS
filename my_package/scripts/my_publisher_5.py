#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion
from math import atan2
from nav_msgs.msg import Odometry
from Main import *

class TurtlebotPathFollower:
    def __init__(self):
        rospy.init_node('turtlebot_path_follower', anonymous=True)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.path = []

    def follow_path(self, path):
        self.path = path
        rate = rospy.Rate(10)  # 10 Hz
        rospy.loginfo("Following path...")

        for point in self.path:
            goal_x, goal_y = point

            while not rospy.is_shutdown():
                current_position = self.get_current_position()
                distance_to_goal = ((current_position[0] - goal_x) ** 2 +
                                    (current_position[1] - goal_y) ** 2) ** 0.5

                if distance_to_goal < 0.1:  # Tolerance for goal position
                    break  # Move to the next point in the path

                # Calculate angle to the goal
                theta = atan2(goal_y - current_position[1], goal_x - current_position[0])
                current_orientation = self.get_current_orientation()
                euler = euler_from_quaternion(current_orientation)
                angular_velocity = 3 * (theta - euler[2])  # P controller for angular velocity

                # Create Twist message to control linear and angular velocities
                cmd_vel = Twist()
                cmd_vel.linear.x = 0.3  # Linear velocity
                cmd_vel.angular.z = angular_velocity  # Angular velocity

                self.cmd_vel_pub.publish(cmd_vel)
                rate.sleep()

        rospy.loginfo("Path completed.")
        # Stop the Turtlebot
        self.cmd_vel_pub.publish(Twist())

    def get_current_position(self):
        try:
            msg = rospy.wait_for_message('/odom', Odometry, timeout=1)
            return msg.pose.pose.position.x, msg.pose.pose.position.y
        except rospy.ROSException:
            rospy.logwarn("Failed to get current position. Returning (0, 0).")
            return 0, 0

    def get_current_orientation(self):
        try:
            msg = rospy.wait_for_message('/odom', Odometry, timeout=1)
            return (
                msg.pose.pose.orientation.x,
                msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z,
                msg.pose.pose.orientation.w
            )
        except rospy.ROSException:
            rospy.logwarn("Failed to get current orientation. Returning default orientation.")
            return 0, 0, 0, 1

if __name__ == '__main__':
    try:
        path_follower = TurtlebotPathFollower()
        #Optimal path as received from the A* algorithm
        optimal_path = [(1, 1, 0), (2.7, 1.0, 0), (4.2, 1.9, 75), (5.5, 3.1, 0), (7.0, 4.0, 75), (7.5, 6.0, 75), (7.9, 7.6, 75), (9.2, 8.8, 0)]
        for idx, each in enumerate(optimal_path):
            optimal_path[idx] = (each[0]-5, each[1]-5)
        path_follower.follow_path(optimal_path)
    except rospy.ROSInterruptException:
        pass
