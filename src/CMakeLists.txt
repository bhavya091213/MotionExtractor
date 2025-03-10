cmake_minimum_required(VERSION 3.10)
project(videostabilizer)

# Set C++ standard to C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Find OpenCV
set(OpenCV_DIR /opt/homebrew/Cellar/opencv/4.11.0_1/share/OpenCV)
find_package(OpenCV REQUIRED)

# Include OpenCV headers
include_directories(${OpenCV_INCLUDE_DIRS})

# Add executable
add_executable(videostabilizer main.cpp)

# Link OpenCV and VidStab libraries
target_link_libraries(videostabilizer ${OpenCV_LIBS} ${VIDSTAB_LIB})
