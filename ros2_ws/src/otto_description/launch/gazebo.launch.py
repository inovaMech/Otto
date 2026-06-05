"""
gazebo.launch.py
Simulação do Otto no Gazebo Harmonic.
Spawn em z=0.075m para pousar corretamente no chão.
Uso: ros2 launch otto_description gazebo.launch.py
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg = get_package_share_directory('otto_description')
    urdf_file = os.path.join(pkg, 'urdf', 'otto.urdf')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # Altura de spawn: pés chegam a z=-0.070m a partir do base_link,
    # +5mm de margem para não penetrar o chão
    spawn_z = '0.075'

    # Argumentos
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty',
        description='World do Gazebo (empty, ground_plane, etc)'
    )

    # Gazebo Harmonic
    gz_sim = ExecuteProcess(
        cmd=['gz', 'sim', '-r', 'empty.sdf'],
        output='screen'
    )

    # Publicar robot_description no tópico ROS 2
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    # Spawn do Otto no Gazebo via ros_gz_sim
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='spawn_otto',
        arguments=[
            '-name', 'iMech_Otto',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', spawn_z,   # pousa corretamente no chão
            '-R', '0.0',
            '-P', '0.0',
            '-Y', '0.0',
        ],
        output='screen'
    )

    # Bridge ROS 2 <-> Gazebo para tópicos essenciais
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='gz_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/model/iMech_Otto/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
        ],
        output='screen'
    )

    return LaunchDescription([
        world_arg,
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
    ])
