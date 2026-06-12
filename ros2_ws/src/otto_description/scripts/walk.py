#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import time

class OttoWalk(Node):
    def __init__(self):
        super().__init__('otto_walk')
        self.pub = self.create_publisher(
            Float64MultiArray,
            '/otto_position_controller/commands',
            10
        )
        # Ordem: [foot_left, foot_right, leg_left, leg_right]
        self.posturas = [
            [0.0,  0.0,  0.0,  0.0],   # neutro
            [ 0.5, 0.0,  0.0,  0.0],   # pe esquerdo abaixa
            [ 0.5, 0.0,  0.5,  0.0],   # perna esquerda avança
            [0.0,  0.0,  0.5,  0.0],   # pe esquerdo sobe
            [0.0,  0.0,  0.0,  0.0],   # perna esquerda volta neutro
            [0.0,  0.5,  0.0,  0.0],   # pe direito abaixa
            [0.0,  0.5,  0.0, -0.5],   # perna direita avança
            [0.0,  0.0,  0.0, -0.5],   # pe direito sobe
            [0.0,  0.0,  0.0,  0.0],   # perna direita volta neutro
        ]
        self.step_duration = 0.5
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.current_step = 0
        self.last_time = time.time()
        self.get_logger().info('Otto walk node iniciado')

    def timer_callback(self):
        now = time.time()
        if now - self.last_time >= self.step_duration:
            postura = self.posturas[self.current_step]
            msg = Float64MultiArray()
            msg.data = postura
            self.pub.publish(msg)
            self.get_logger().info(f'Postura {self.current_step}: {postura}')
            self.current_step = (self.current_step + 1) % len(self.posturas)
            self.last_time = now

def main(args=None):
    rclpy.init(args=args)
    node = OttoWalk()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
