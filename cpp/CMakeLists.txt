cmake_minimum_required (VERSION 2.6)

project (grpc4bmi)

add_compile_options(-std=c++11)

find_package(Protobuf REQUIRED)
find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin REQUIRED)
find_library(GRPCPP_UNSECURE grpc++_unsecure)
find_library(GRPCLIB grpc)
find_library(BMIC bmic)

set(PROTO_PATH "${CMAKE_SOURCE_DIR}/../proto/grpc4bmi")
add_custom_command(
    OUTPUT bmi.pb.h bmi.pb.cc 
    COMMAND ${PROTOBUF_PROTOC_EXECUTABLE} 
    ARGS "--proto_path=${PROTO_PATH}"
         "--cpp_out=${CMAKE_CURRENT_BINARY_DIR}"
         "${PROTO_PATH}/bmi.proto"
    )
add_custom_command(
    OUTPUT bmi.grpc.pb.h bmi.grpc.pb.cc 
    COMMAND ${PROTOBUF_PROTOC_EXECUTABLE} 
    ARGS "--proto_path=${PROTO_PATH}"
         "--grpc_out=${CMAKE_CURRENT_BINARY_DIR}"
         "--plugin=protoc-gen-grpc=${GRPC_CPP_PLUGIN}"
         "${PROTO_PATH}/bmi.proto"
    )
set(GRPC_SRC_FILES ${CMAKE_CURRENT_BINARY_DIR}/bmi.pb.h ${CMAKE_CURRENT_BINARY_DIR}/bmi.pb.cc
                   ${CMAKE_CURRENT_BINARY_DIR}/bmi.grpc.pb.h ${CMAKE_CURRENT_BINARY_DIR}/bmi.grpc.pb.cc)
link_libraries(GRPCPP_UNSECURE GRPC BMIC ${PROTOBUF_LIBRARY})
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/bmi-c/bmi)
include_directories(${CMAKE_CURRENT_BINARY_DIR})
add_library (grpc4bmi SHARED bmi_class.h bmi_cpp_extension.h bmi_cpp_extension.cc
    bmi_c_wrapper.h bmi_c_wrapper.cc bmi_grpc_server.cc bmi_grpc_server.h ${GRPC_SRC_FILES})

add_subdirectory (test bmi-c)

include (CTest)

