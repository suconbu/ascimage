cmake_minimum_required(VERSION 3.5)
project(imageutil)
add_library(${PROJECT_NAME} SHARED main.cpp)
set_target_properties(${PROJECT_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)

