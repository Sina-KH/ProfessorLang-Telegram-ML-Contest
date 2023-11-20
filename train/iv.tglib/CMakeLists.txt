cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_CXX_FLAGS "-O3 -Wall -Wextra")
#set(CMAKE_CXX_FLAGS_DEBUG "-g -Wall -Wextra")

project(tglang)
project(${PROJECT_NAME} VERSION 2.0.0 LANGUAGES CXX)

add_library(${PROJECT_NAME} SHARED tglang.cpp utils.cpp features.cpp)
