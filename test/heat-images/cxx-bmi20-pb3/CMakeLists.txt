cmake_minimum_required(VERSION 3.0)
project(run_heat_bmi_model)

find_package(PkgConfig REQUIRED)
pkg_check_modules(BMI REQUIRED bmic bmicxx)
pkg_check_modules(GRPC4BMI REQUIRED protobuf grpc++ grpc++_unsecure grpc++_reflection grpc4bmi heatcxx)

# /cpp/bmi_grpc_server.h uses `#include "bmi-cxx/bmi.hxx"` while bmi-cxx installs /usr/local/include/bmi.hxx
# so use grpc4bmi scr code to have include in sub dir

add_executable(run_heat_bmi_model run_heat_bmi_model.cc "/opt/grpc4bmi/cpp/bmi-c/bmi.h")

target_include_directories(run_heat_bmi_model PRIVATE "/opt/grpc4bmi/cpp")

target_link_libraries(run_heat_bmi_model
                      ${GRPC4BMI_LINK_LIBRARIES}
                      )
