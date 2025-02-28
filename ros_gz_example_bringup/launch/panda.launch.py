import os
import launch_ros

from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

def generate_launch_description():
    pkg_project_description = get_package_share_directory('ros_gz_example_description')
    sdf_file  =  os.path.join(pkg_project_description, 'models', 'panda_moveit', 'model.sdf')
    with open(sdf_file, 'r') as infp:
        robot_description = infp.read()

    pkg_project_gazebo = get_package_share_directory('ros_gz_example_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            pkg_project_gazebo,
            'worlds',
            'panda.sdf'
        ])}.items(),
    )

    pkg_project_bringup = get_package_share_directory('ros_gz_example_bringup')

    # # Bridge ROS topics and Gazebo messages for establishing communication
    # bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     parameters=[{
    #         'config_file': os.path.join(pkg_project_bringup, 'config', 'tm5-700_bridge.yaml'),
    #         'qos_overrides./tf_static.publisher.durability': 'transient_local',
    #     }],
    #     output='screen'
    # )

    # rviz_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     # arguments=['-d', os.path.join(rviz_share, 'config', 'rrbot.rviz')], # change last arg to actual robot name
    #     condition=IfCondition(LaunchConfiguration('rviz'))
    # )

    # Start Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_description}
        ]
    )

    return LaunchDescription([
        # Start Gazebo Fortress
        gz_sim,
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Open RViz.'),
        robot_state_publisher,
    ])