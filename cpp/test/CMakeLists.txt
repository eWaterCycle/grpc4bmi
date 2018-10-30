cmake_minimum_required (VERSION 2.6)
add_executable(test_cpp_extension test_bmi_cpp_extension.cc bmi_test_extension.cc ${CMAKE_CURRENT_SOURCE_DIR}/../bmi_cpp_extension.cc)
target_include_directories(test_cpp_extension PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/..)
include (CTest)
add_test(NAME test_cpp_extension COMMAND test_cpp_extension)

