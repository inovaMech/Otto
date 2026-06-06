#!/bin/bash
# ============================================================
# Entrypoint — Otto Sim
# ============================================================

set -e

# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Build do workspace se ainda não foi feito
if [ ! -d "$ROS2_WS/install" ]; then
    echo "============================================"
    echo "  Primeiro uso: compilando workspace ROS 2..."
    echo "============================================"
    cd $ROS2_WS
    colcon build --symlink-install 2>&1 | tail -20
    echo "Build concluído."
fi

# Source do workspace do aluno
if [ -f "$ROS2_WS/install/setup.bash" ]; then
    source $ROS2_WS/install/setup.bash
fi

# Exportar GAZEBO_MODEL_PATH
export GAZEBO_MODEL_PATH=$ROS2_WS/install/otto_description/share/otto_description/models:$GAZEBO_MODEL_PATH

# Adicionar ao bashrc para sessões interativas
grep -qxF 'source /opt/ros/jazzy/setup.bash' ~/.bashrc || \
    echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc

grep -qxF 'source /ros2_ws/install/setup.bash' ~/.bashrc || \
    echo '[ -f /ros2_ws/install/setup.bash ] && source /ros2_ws/install/setup.bash' >> ~/.bashrc

echo ""
echo "============================================"
echo "  Otto Sim — Ambiente pronto!"
echo "  ROS 2 Jazzy + Gazebo Harmonic + Octave"
echo ""
echo "  Comandos úteis:"
echo "    check_urdf src/otto_description/urdf/otto.urdf"
echo "    ros2 launch otto_description display.launch.py"
echo "    ros2 launch otto_description gazebo.launch.py"
echo "============================================"
echo ""

exec "$@"