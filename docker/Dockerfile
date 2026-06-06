FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bahia

RUN apt-get update && apt-get install -y \
    curl wget git nano vim \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    xterm mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Adicionar repositório OSRF para Gazebo Harmonic
RUN curl -sSL https://packages.osrfoundation.org/gazebo.gpg \
    -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
    http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/gazebo-stable.list

RUN apt-get update && apt-get install -y \
    gz-harmonic \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-gz-ros2-control \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    ros-jazzy-xacro \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-rviz2 \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    liburdfdom-tools \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q https://github.com/openrr/urdf-viz/releases/download/v0.42.0/urdf-viz-x86_64-unknown-linux-gnu.tar.gz \
    -O /tmp/urdf-viz.tar.gz \
    && tar -xzf /tmp/urdf-viz.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/urdf-viz \
    && rm /tmp/urdf-viz.tar.gz

RUN apt-get update && apt-get install -y \
    octave \
    octave-control \
    octave-signal \
    octave-statistics \
    octave-symbolic \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true && rosdep update

ENV ROS_DOMAIN_ID=0
ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
ENV GZ_VERSION=harmonic
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1
ENV ROS2_WS=/ros2_ws

WORKDIR $ROS2_WS

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
