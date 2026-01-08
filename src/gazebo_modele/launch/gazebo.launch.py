
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2025 <Ming2zun:https://github.com/Ming2zun/Pure-tracking-slam-automatic-navigation-system>
#                <喵了个水蓝蓝:https://www.bilibili.com/video/BV1kzEwzuEFw?spm_id_from=333.788.videopod.sections&vd_source=134c12873ff478ea447a06d652426f8f>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# ============================================================================
# 导入必要的Python模块
# ============================================================================

import os
# os: 操作系统接口模块，用于处理文件路径等操作

from launch import LaunchDescription
# LaunchDescription: ROS2 launch系统的核心类，用于描述要启动的所有节点和进程

from launch.actions import ExecuteProcess
# ExecuteProcess: 用于在launch文件中执行外部命令/程序（比如启动Gazebo）

from launch_ros.actions import Node
# Node: 用于启动ROS2节点的类，每个ROS2程序都是一个节点

from launch_ros.substitutions import FindPackageShare
# FindPackageShare: 用于查找ROS2包的安装路径（自动找到包的位置，不需要硬编码路径）



# ============================================================================
# 主函数：生成launch描述
# ============================================================================
# 这个函数是launch文件的入口点，ROS2会自动调用它来启动所有节点
def generate_launch_description():
    # ========================================================================
    # 第一步：定义基本参数（可以理解为"配置变量"）
    # ========================================================================
    # 设置 Gazebo 模型路径（让 Gazebo 能找到 SU7 的 mesh 文件）
    su7_model_dir = '/home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system/src/su7_gazebo/gazebo_four_wheeled_vehicle/four_wheeled_vehicle_plugin/models'
    os.environ['GAZEBO_MODEL_PATH'] = f"{os.environ.get('GAZEBO_MODEL_PATH', '')}:{su7_model_dir}"
    
    # 设置 Gazebo 插件路径（让 Gazebo 能找到 SU7 的插件）
    # 插件编译后会在 install/four_wheeled_vehicle/lib/four_wheeled_vehicle/ 目录下
    su7_plugin_dir = '/home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system/install/four_wheeled_vehicle/lib/four_wheeled_vehicle'
    os.environ['GAZEBO_PLUGIN_PATH'] = f"{os.environ.get('GAZEBO_PLUGIN_PATH', '')}:{su7_plugin_dir}"
    # 机器人在Gazebo中的名字（可以自定义，比如改成'my_robot'）
    robot_name_in_model = 'XIAOMI-SU7'
    
    # 当前ROS2包的名字（这个文件所在的包）
    package_name = 'gazebo_modele' 

    # URDF文件名（URDF是描述机器人外观和结构的文件，类似"机器人的说明书"）
    su7_model_path = '/home/talooulu/ROS2/Pure-tracking-slam-automatic-navigation-system/src/su7_gazebo/gazebo_four_wheeled_vehicle/four_wheeled_vehicle_plugin/models/four_wheeled_vehicle/model_sensor.sdf'
   
    # 创建一个空的launch描述对象，后续会把所有要启动的节点添加进去
    ld = LaunchDescription()
    
    # ========================================================================
    # 第二步：查找文件路径（自动找到包安装后的位置）
    # ========================================================================
    
    # 找到gazebo_modele包的安装路径
    # 例如：/home/user/workspace/install/gazebo_modele/share/gazebo_modele
    pkg_share = FindPackageShare(package=package_name).find(package_name) 
    
    # 注意：SU7 使用 SDF 格式，不是 URDF，所以不需要 urdf_model_path
    # 如果需要使用原来的 fishbot（URDF），取消下面的注释：
    # urdf_name = "model.urdf"
    # urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')
    
    # 拼接Gazebo世界文件的完整路径（世界文件定义了仿真环境，比如房间、障碍物等）
    # 例如：/home/user/.../gazebo_modele/world/3d.world
    gazebo_world_path = os.path.join(pkg_share, 'world/3d.world')

    # ========================================================================
    # 第三步：创建要启动的节点和进程
    # ========================================================================
    
    # ------------------------------------------------------------------------
    # 节点1：启动Gazebo仿真器
    # ------------------------------------------------------------------------
    # ExecuteProcess用于执行外部程序（不是ROS2节点，而是普通程序）
    start_gazebo_cmd = ExecuteProcess(
        # cmd: 要执行的命令，相当于在终端输入的命令
        cmd=[
            'gazebo',                    # Gazebo可执行程序
            '--verbose',                 # 详细输出模式（显示更多信息，方便调试）
            '-s', 'libgazebo_ros_init.so',      # 加载ROS插件：初始化ROS接口（让Gazebo能和ROS2通信）
            '-s', 'libgazebo_ros_factory.so',   # 加载ROS插件：启用实体生成功能（可以通过ROS服务生成机器人）
            gazebo_world_path            # 要加载的世界文件路径（3d.world）
        ],
        output='screen'  # 将输出显示在终端屏幕上（方便查看日志）
    )
        
    # ------------------------------------------------------------------------
    # 节点2：在Gazebo中生成机器人模型
    # ------------------------------------------------------------------------
    # 这个节点会调用Gazebo的服务，把URDF文件描述的机器人"放置"到仿真世界中
    spawn_entity_cmd = Node(
        package='gazebo_ros',           # 包名：gazebo_ros（Gazebo的ROS接口包）
        executable='spawn_entity.py',    # 可执行文件：生成实体的Python脚本
        arguments=[
            '-entity', robot_name_in_model,
            '-file', su7_model_path,  # 使用 SDF 文件路径
            '-x', '0.0', '-y', '0.0', '-z', '1.0'  # 初始位置（可选）
        ],
        output='screen'  # 输出到屏幕
    )
	
    # ------------------------------------------------------------------------
    # 节点3：发布机器人状态（Robot State Publisher）
    # ------------------------------------------------------------------------
    # 注意：SU7 使用 SDF 格式，但 RViz 需要 URDF 来显示模型
    # 所以使用一个简化的 URDF 文件用于 RViz 显示
    su7_rviz_urdf_path = os.path.join(pkg_share, 'urdf/su7_rviz.urdf')
    start_robot_state_publisher_cmd = Node(
        package='robot_state_publisher',     # 包名：robot_state_publisher
        executable='robot_state_publisher',  # 可执行文件：机器人状态发布器
        arguments=[su7_rviz_urdf_path],     # 参数：用于 RViz 显示的简化 URDF 文件
        name='robot_state_publisher'
    )
    
    # ------------------------------------------------------------------------
    # 节点4：关节状态发布器（带GUI界面）
    # ------------------------------------------------------------------------
    # 这个节点提供一个图形界面，可以手动调整机器人的关节角度
    # 主要用于调试和测试，可以看到机器人各个关节的状态
    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher_gui',  # 包名：带GUI的关节状态发布器
    #     executable='joint_state_publisher_gui', # 可执行文件
    #     name='joint_state_publisher_gui',       # 节点名称（可以自定义）
    #     arguments=[urdf_model_path]             # 参数：URDF文件路径
    # )
    
    # ------------------------------------------------------------------------
    # 节点5-7：发布静态TF变换（坐标变换）
    # ------------------------------------------------------------------------
    # TF（Transform）是ROS2中用于描述坐标系之间关系的系统
    # 静态TF变换：两个坐标系之间的位置和姿态关系是固定的，不会改变
    
    # 节点5：odom → base_footprint 的变换
    # 作用：连接里程计坐标系和机器人脚部坐标系
    # 参数说明：x, y, z, roll, pitch, yaw, 父坐标系, 子坐标系
    # 这里都是0，表示两个坐标系重合（没有偏移和旋转）
    # fake_basel_cmd4 = Node(
    #     package='tf2_ros',                    # 包名：TF2（ROS2的坐标变换库）
    #     executable='static_transform_publisher', # 可执行文件：静态变换发布器
    #     output='screen',
    #     arguments=[
    #         '0', '0', '0',                    # x, y, z 偏移（米）：0表示没有偏移
    #         '0', '0', '0',                    # roll, pitch, yaw 旋转（弧度）：0表示没有旋转
    #         'odom',                           # 父坐标系：里程计坐标系（基于轮子编码器的坐标系）
    #         'base_footprint'                  # 子坐标系：机器人脚部坐标系（机器人接触地面的点）
    #     ]
    # )
    
    # 节点6：base_footprint → base_link 的变换
    # 作用：连接机器人脚部和机器人本体
    # z=0.1 表示机器人本体比脚部高0.1米（机器人有一定高度）
    # fake_basel_cmd5 = Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     output='screen',
    #     arguments=[
    #         '0', '0', '0.1',                  # x, y, z：z=0.1表示向上偏移0.1米
    #         '0', '0', '0',                    # roll, pitch, yaw：无旋转
    #         'base_footprint',                  # 父坐标系：机器人脚部
    #         'base_link'                        # 子坐标系：机器人本体（通常是机器人的中心）
    #     ]
    # )
    # 添加新的：odom → base_link（直接连接）
    fake_basel_cmd_odom_base = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link']
    )
    
    # SU7 传感器 TF 发布器（用于 RViz 显示）
    # 注意：这些位置需要与 SDF 文件中的 joint pose 保持一致
    stf_lidar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='stf_lidar3d',
        arguments=['1.30', '0', '0.95', '0', '0', '0', 'base_link', 'lidar3d_link'],
        output='screen'
    )
    stf_gps = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='stf_gps',
        arguments=['-0.50', '0', '0.95', '0', '0', '0', 'base_link', 'gps_link'],
        output='screen'
    )
    stf_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='stf_imu',
        arguments=['0', '0', '0.30', '0', '0', '0', 'base_link', 'imu_link'],
        output='screen'
    )
    stf_camera = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='stf_camera',
        arguments=['2.20', '0', '0.60', '0', '0', '0', 'base_link', 'camera_link'],
        output='screen'
    )
    # 节点7：map → odom 的变换
    # 作用：连接地图坐标系和里程计坐标系
    # 注意：这里设置为0，表示初始时两个坐标系重合
    # 在实际SLAM中，这个变换应该由SLAM算法动态计算和发布
    fake_basel_cmd6 = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        output='screen',
        arguments=[
            '0', '0', '0.0',                  # x, y, z：无偏移
            '0', '0', '0',                    # roll, pitch, yaw：无旋转
            'map',                            # 父坐标系：地图坐标系（全局固定坐标系）
            'odom'                            # 子坐标系：里程计坐标系
        ]
    )
    
    # ========================================================================
    # 第四步：将所有节点添加到launch描述中
    # ========================================================================
    # 只有添加到ld中的节点才会被启动
    # 添加顺序很重要：Gazebo必须先启动，然后才能生成机器人
    
    # 首先启动Gazebo仿真器（必须最先启动）
    ld.add_action(start_gazebo_cmd)
    
    # 在Gazebo中生成机器人模型（需要等Gazebo启动后才能执行）
    ld.add_action(spawn_entity_cmd)
    
    # 发布机器人状态的TF变换（用于 RViz 显示）
    # 注意：使用简化的 URDF 文件，仅用于 RViz 可视化
    ld.add_action(start_robot_state_publisher_cmd)
    
    # 启动关节状态发布器GUI（可选，用于调试）
    # ld.add_action(joint_state_publisher_node)

    # 发布静态TF变换（建立坐标系之间的连接）
    # 这些变换的顺序不重要，因为它们都是独立的
    # ld.add_action(fake_basel_cmd4)  # odom → base_footprint
    # ld.add_action(fake_basel_cmd5)  # base_footprint → base_link
    ld.add_action(fake_basel_cmd_odom_base)  # odom → base_link
    ld.add_action(fake_basel_cmd6)  # map → odom
    
    # SU7 传感器 TF（用于 RViz 显示）
    ld.add_action(stf_lidar)
    ld.add_action(stf_gps)
    ld.add_action(stf_imu)
    ld.add_action(stf_camera)

    # ========================================================================
    # 返回launch描述对象
    # ========================================================================
    # ROS2会自动读取这个返回值，然后启动里面定义的所有节点
    return ld


# ============================================================================
# 总结：这个launch文件做了什么？
# ============================================================================
# 1. 启动Gazebo仿真器，加载3D世界环境
# 2. 在Gazebo中生成机器人模型（根据URDF文件）
# 3. 发布机器人的TF变换（让其他节点知道机器人各部分的位置）
# 4. 建立坐标系之间的连接（map → odom → base_footprint → base_link）
# 
# 运行方式：
# ros2 launch gazebo_modele gazebo.launch.py
# 
# 运行后你会看到：
# - Gazebo窗口打开，显示3D仿真环境
# - 机器人出现在环境中
# - 终端显示各个节点的启动信息
# ============================================================================