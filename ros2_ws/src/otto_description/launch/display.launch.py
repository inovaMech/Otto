"""
display.launch.py
Visualização do Otto no RViz2 com controle manual das juntas.
Uso: ros2 launch otto_description display.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('otto_description')
    urdf_file = os.path.join(pkg, 'urdf', 'otto.urdf')
    rviz_config = os.path.join(pkg, 'rviz', 'otto.rviz')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # Argumento para habilitar/desabilitar GUI das juntas
    gui_arg = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Abrir joint_state_publisher_gui'
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=__import__('launch.conditions', fromlist=['IfCondition']).IfCondition(
            LaunchConfiguration('gui')
        )
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        gui_arg,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz2,
    ])
