#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import sys

class OttoWalk(Node):
    def __init__(self):
        super().__init__('otto_walk')
        self.pub = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(0.02, self.update)  # 50Hz
        self.t = 0.0
        self.walking = False
        self.get_logger().info('OttoWalk ready. Use: ros2 topic pub /otto/cmd std_msgs/msg/String "data: walk"')

        self.cmd_sub = self.create_subscription(
            __import__('std_msgs.msg', fromlist=['String']).String,
            '/otto/cmd', self.cmd_callback, 10)

    def cmd_callback(self, msg):
        if msg.data == 'walk':
            self.walking = True
            self.get_logger().info('Walking!')
        elif msg.data == 'stop':
            self.walking = False
            self.t = 0.0
            self.get_logger().info('Stopped.')

    def update(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['leg_right_joint', 'leg_left_joint', 'foot_right_joint', 'foot_left_joint']

        if self.walking:
            A = 0.3   # amplitude pernas (rad)
            Af = 0.2  # amplitude pés (rad)
            T = 1.0   # período (s)
            w = 2 * math.pi / T

            leg_r  =  A  * math.sin(w * self.t)
            leg_l  = -A  * math.sin(w * self.t)
            foot_r =  Af * math.sin(w * self.t + math.pi/2)
            foot_l = -Af * math.sin(w * self.t + math.pi/2)

            self.t += 0.02
        else:
            leg_r = leg_l = foot_r = foot_l = 0.0

        msg.position = [leg_r, leg_l, foot_r, foot_l]
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = OttoWalk()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
