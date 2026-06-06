cmake_minimum_required(VERSION 3.8)
project(otto_description)

find_package(ament_cmake REQUIRED)

# Instala os recursos colocando cada pasta inteira no diretório share
install(
  DIRECTORY launch urdf meshes rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
