cmake_minimum_required (VERSION 3.6)

project (grpc4bmi C CXX)
set (GRPC4BMI_VERSION 0.2)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/grpc4bmi.pc.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/grpc4bmi.pc)

if (NOT DEFINED CMAKE_CXX_STANDARD)
  set (CMAKE_CXX_STANDARD 14)
endif()

find_package(Threads REQUIRED)
find_package(Protobuf REQUIRED)
message(STATUS "Using protobuf ${Protobuf_VERSION}")
find_program(GRPC_CPP_PLUGIN grpc_cpp_plugin REQUIRED)
find_library(GRPCREFLECTION grpc++_reflection)
find_library(GRPCLIB grpc CONFIG REQUIRED)
message(STATUS "Using gRPC ${GRPCLIB_VERSION}")
find_package(PkgConfig REQUIRED)
pkg_check_modules(ABSL_CHECK REQUIRED IMPORTED_TARGET absl_check)
pkg_check_modules(BMI REQUIRED IMPORTED_TARGET bmic bmicxx)
message(STATUS "Using BMI ${BMI_VERSION}")

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

include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(${BMI_INCLUDE_DIRS})

add_library (grpc4bmi SHARED bmi_cpp_extension.h bmi_cpp_extension.cc
    bmi_c_wrapper.h bmi_c_wrapper.cc bmi_grpc_server.cc bmi_grpc_server.h ${GRPC_SRC_FILES} ${GRPC_HDR_FILES})

target_link_libraries(
    grpc4bmi
    ${GRPCREFLECTION}
    ${GRPC}
    ${PROTOBUF_LIBRARY}
    ${ABSL_CHECK_LINK_LIBRARIES}
)
set_target_properties(grpc4bmi PROPERTIES PUBLIC_HEADER "bmi_cpp_extension.h;bmi_c_wrapper.h;bmi_grpc_server.h;${GRPC_HDR_FILES}")
add_subdirectory (test)

include (CTest)

install(TARGETS grpc4bmi LIBRARY DESTINATION lib PUBLIC_HEADER DESTINATION include)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/grpc4bmi.pc DESTINATION lib/pkgconfig)
