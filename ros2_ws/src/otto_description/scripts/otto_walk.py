#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import math
import time

class OttoWalk(Node):
    def __init__(self):
        super().__init__('otto_walk')

        self.pub_leg_r  = self.create_publisher(Float64, '/leg_right_joint/cmd', 10)
        self.pub_leg_l  = self.create_publisher(Float64, '/leg_left_joint/cmd', 10)
        self.pub_foot_r = self.create_publisher(Float64, '/foot_right_joint/cmd', 10)
        self.pub_foot_l = self.create_publisher(Float64, '/foot_left_joint/cmd', 10)
        self.pub_js     = self.create_publisher(JointState, '/joint_states', 10)

        self.t = 0.0
        self.walking = False

        self.cmd_sub = self.create_subscription(
            __import__('std_msgs.msg', fromlist=['String']).String,
            '/otto/cmd', self.cmd_callback, 10)

        self.get_logger().info('Enviando posição zero inicial...')
        for _ in range(20):
            self.send_zero()
            time.sleep(0.05)

        self.get_logger().info('OttoWalk pronto.')
        self.timer = self.create_timer(0.02, self.update)

    def send_zero(self):
        z = Float64()
        z.data = 0.0
        for pub in [self.pub_leg_r, self.pub_leg_l, self.pub_foot_r, self.pub_foot_l]:
            pub.publish(z)

    def cmd_callback(self, msg):
        if msg.data == 'walk':
            self.walking = True
            self.t = 0.0
            self.get_logger().info('Walking!')
        elif msg.data == 'stop':
            self.walking = False
            self.send_zero()
            self.get_logger().info('Stopped.')

    def update(self):
        if self.walking:
            A  = 0.3
            Af = 0.2
            w  = 2 * math.pi / 1.0

            leg_r  =  A  * math.sin(w * self.t)
            leg_l  = -A  * math.sin(w * self.t)
            foot_r =  Af * math.sin(w * self.t + math.pi / 2)
            foot_l = -Af * math.sin(w * self.t + math.pi / 2)
            self.t += 0.02
        else:
            leg_r = leg_l = foot_r = foot_l = 0.0

        def pub_gz(publisher, val):
            m = Float64()
            m.data = val
            publisher.publish(m)

        pub_gz(self.pub_leg_r,  leg_r)
        pub_gz(self.pub_leg_l,  leg_l)
        pub_gz(self.pub_foot_r, foot_r)
        pub_gz(self.pub_foot_l, foot_l)

        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name     = ['leg_right_joint', 'leg_left_joint', 'foot_right_joint', 'foot_left_joint']
        js.position = [leg_r, leg_l, foot_r, foot_l]
        self.pub_js.publish(js)

def main():
    rclpy.init()
    node = OttoWalk()
    rclpy.spin(node)

if __name__ == '__main__':
    main()