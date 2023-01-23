cmake_minimum_required(VERSION 3.0)
project(run_heat_bmi_model)

find_package(PkgConfig REQUIRED)
pkg_check_modules(GRPC4BMI REQUIRED protobuf grpc++ grpc4bmi bmicxx bmic heatcxx)

# /cpp/bmi_grpc_server.h uses `#include "bmi-cxx/bmi.hxx"` while bmi-cxx installs /usr/local/include/bmi.hxx
# so use grpc4bmi scr code to have include in sub dir

add_executable(run_heat_bmi_model run_heat_bmi_model.cc "/opt/grpc4bmi/cpp/bmi-c/bmi.h")

target_include_directories(run_heat_bmi_model PRIVATE "/opt/grpc4bmi/cpp")

# target_link_libraries(run_heat_bmi_model
#                       ${GRPC4BMI_LINK_LIBRARIES}
#                       )

# /src/test/heat-images/cxx-bmi20-pb3/build# make
# Scanning dependencies of target run_heat_bmi_model
# [ 50%] Building CXX object CMakeFiles/run_heat_bmi_model.dir/run_heat_bmi_model.cc.o
# [100%] Linking CXX executable run_heat_bmi_model
# /usr/bin/ld: CMakeFiles/run_heat_bmi_model.dir/run_heat_bmi_model.cc.o: in function `main':
# run_heat_bmi_model.cc:(.text+0x3c): undefined reference to `run_bmi_server(bmi::Bmi*, int, char**)'
# /usr/bin/ld: CMakeFiles/run_heat_bmi_model.dir/run_heat_bmi_model.cc.o: in function `BmiHeat::BmiHeat()':
# run_heat_bmi_model.cc:(.text._ZN7BmiHeatC2Ev[_ZN7BmiHeatC5Ev]+0x1e): undefined reference to `vtable for BmiHeat'
# /usr/bin/ld: run_heat_bmi_model.cc:(.text._ZN7BmiHeatC2Ev[_ZN7BmiHeatC5Ev]+0x35): undefined reference to `heat::Heat::Heat()'
# /usr/bin/ld: run_heat_bmi_model.cc:(.text._ZN7BmiHeatC2Ev[_ZN7BmiHeatC5Ev]+0x13e): undefined reference to `heat::Heat::~Heat()'
# collect2: error: ld returned 1 exit status
# make[2]: *** [CMakeFiles/run_heat_bmi_model.dir/build.make:84: run_heat_bmi_model] Error 1
# make[1]: *** [CMakeFiles/Makefile2:73: CMakeFiles/run_heat_bmi_model.dir/all] Error 2
# make: *** [Makefile:84: all] Error 2
