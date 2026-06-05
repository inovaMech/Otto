cmake_minimum_required(VERSION 3.8)
project(otto_description)

find_package(ament_cmake REQUIRED)

# Instala pastas de recursos
install(
  DIRECTORY urdf meshes launch rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
