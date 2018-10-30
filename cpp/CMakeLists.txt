cmake_minimum_required (VERSION 2.6)
project (grpc4bmi)
add_library (grpc4bmi SHARED bmi_class.h bmi_cpp_extension.h bmi_cpp_extension.cc
    bmi_c_wrapper.h bmi_c_wrapper.cc bmi_grpc_server.cc bmi_grpc_server.h)
target_include_directories(grpc4bmi PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
add_custom_target(bmi.pb.cc COMMAND protoc -I ${CMAKE_CURRENT_SOURCE_DIR}/../proto/grpc4bmi --cpp_out=. ${CMAKE_CURRENT_SOURCE_DIR}/../proto/grpc4bmi/bmi.proto)
add_dependencies(grpc4bmi bmi.pb.cc)
add_custom_target(bmi.grpc.pb.cc COMMAND protoc -I ${CMAKE_CURRENT_SOURCE_DIR}/../proto/grpc4bmi --grpc_out=.
    --plugin=protoc-gen-grpc=/usr/local/bin/grpc_cpp_plugin ${CMAKE_CURRENT_SOURCE_DIR}/../proto/grpc4bmi/bmi.proto)
add_dependencies(grpc4bmi bmi.grpc.pb.cc)
add_subdirectory (test bmi-c)
include (CTest)

