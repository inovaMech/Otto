#!/usr/bin/env python3

from launch_ros.parameter_descriptions import ParameterValue
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory, get_package_prefix

def generate_launch_description():

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="cat")]),
            " ",
            PathJoinSubstitution([FindPackageShare("otto"), "urdf", "otto.urdf"]),
        ]
    )

    robot_description = {"robot_description": ParameterValue(robot_description_content, value_type=str)}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    ###### RVIZ ######
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("otto"), "launch", "urdf.rviz"]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    ###### GAZEBO HARMONIC ######
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                get_package_share_directory("ros_gz_sim"),
                "launch", "gz_sim.launch.py",
            ])
        ]),
        launch_arguments={"gz_args": "-r empty.sdf"}.items(),
    )

    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'otto',
            '-z', '0.033',
            '-Y', '3.1407',
        ],
        output='both'
    )

    gazebo_env = AppendEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        PathJoinSubstitution([get_package_prefix("otto"), "share"])
    )

    ###### BRIDGE ROS2 <-> GAZEBO ######
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        arguments=[
            '/world/empty/model/otto/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        remappings=[
            ('/world/empty/model/otto/joint_state', '/joint_states'),
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo_env,
        robot_state_publisher_node,
        rviz_node,
        gazebo,
        spawn_entity,
        joint_state_publisher_gui_node,
        bridge,
    ])