cmake_minimum_required(VERSION 3.0)
project(run_bmi_server C CXX)

set(_cflags "-ansi -Wall -Wundef -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -O2")
find_package(PkgConfig REQUIRED)
pkg_check_modules(BMIC REQUIRED IMPORTED_TARGET bmic)
message("--   bmic include - ${BMIC_INCLUDE_DIRS}")
include_directories(${BMIC_INCLUDE_DIRS})
pkg_check_modules(GRPC4BMI REQUIRED grpc4bmi heatc)

add_executable(run_bmi_server run_bmi_server.cc)

target_include_directories(run_bmi_server PRIVATE)

target_link_libraries(run_bmi_server
                      ${GRPC4BMI_LINK_LIBRARIES}
                      )

install(TARGETS run_bmi_server
        RUNTIME DESTINATION bin)
