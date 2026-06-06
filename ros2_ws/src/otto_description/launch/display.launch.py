import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    pkg = get_package_share_directory('otto_description')
    urdf_file = os.path.join(pkg, 'urdf', 'otto.urdf')
    rviz_config = os.path.join(pkg, 'rviz', 'otto.rviz')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            condition=IfCondition(LaunchConfiguration('gui'))
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),
    ])
