cmake_minimum_required (VERSION 2.6)

project (grpc4bmi)
set (GRPC4BMI_VERSION 0.2)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/grpc4bmi.pc.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/grpc4bmi.pc)

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
set(GRPC_SRC_FILES ${CMAKE_CURRENT_BINARY_DIR}/bmi.pb.cc ${CMAKE_CURRENT_BINARY_DIR}/bmi.grpc.pb.cc)
set(GRPC_HDR_FILES ${CMAKE_CURRENT_BINARY_DIR}/bmi.pb.h ${CMAKE_CURRENT_BINARY_DIR}/bmi.grpc.pb.h)
link_libraries(${PROTOBUF_LIBRARY} ${GRPCPP_UNSECURE} ${GRPC} ${BMIC})
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/bmi-c)
include_directories(${CMAKE_CURRENT_BINARY_DIR})
add_library (grpc4bmi SHARED bmi_class.h bmi_cpp_extension.h bmi_cpp_extension.cc
    bmi_c_wrapper.h bmi_c_wrapper.cc bmi_grpc_server.cc bmi_grpc_server.h ${GRPC_SRC_FILES} ${GRPC_HDR_FILES})
set_target_properties(grpc4bmi PROPERTIES PUBLIC_HEADER "bmi_class.h;bmi_cpp_extension.h;bmi_c_wrapper.h;bmi_grpc_server.h;${GRPC_HDR_FILES}")
add_subdirectory (test bmi-c)

include (CTest)

install(TARGETS grpc4bmi LIBRARY DESTINATION lib PUBLIC_HEADER DESTINATION include)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/grpc4bmi.pc DESTINATION lib/pkgconfig)
