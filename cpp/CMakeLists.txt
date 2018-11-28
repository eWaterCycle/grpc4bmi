cmake_minimum_required (VERSION 2.6)

project (grpc4bmi)

add_compile_options(-std=c++11)
include_directories(/usr/local/include)
link_directories(/usr/local/lib)

find_package(Protobuf REQUIRED)

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
         "--plugin=protoc-gen-grpc=/usr/local/bin/grpc_cpp_plugin"
         "${PROTO_PATH}/bmi.proto"
    )
set(GRPC_SRC_FILES ${CMAKE_CURRENT_BINARY_DIR}/bmi.pb.h ${CMAKE_CURRENT_BINARY_DIR}/bmi.pb.cc
                   ${CMAKE_CURRENT_BINARY_DIR}/bmi.grpc.pb.h ${CMAKE_CURRENT_BINARY_DIR}/bmi.grpc.pb.cc)

find_library(bmic "/usr/local/lib")
link_libraries(grpc++_unsecure grpc bmic ${PROTOBUF_LIBRARY})
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/bmi-c/bmi)
include_directories(${CMAKE_CURRENT_BINARY_DIR})
add_library (grpc4bmi SHARED bmi_class.h bmi_cpp_extension.h bmi_cpp_extension.cc
    bmi_c_wrapper.h bmi_c_wrapper.cc bmi_grpc_server.cc bmi_grpc_server.h ${GRPC_SRC_FILES})

add_subdirectory (test bmi-c)

include (CTest)
