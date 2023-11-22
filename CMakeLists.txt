cmake_minimum_required(VERSION 3.26)
project(faascale_test)

set(CMAKE_CXX_STANDARD 20)

add_executable(write-overhead E2-write_overhead/test.cpp)
add_executable(userpopulate Evaluation-2/test.cpp)
