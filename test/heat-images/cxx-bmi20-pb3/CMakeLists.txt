cmake_minimum_required(VERSION 3.0)
project(run_bmi_server CXX)

find_package(PkgConfig REQUIRED)
pkg_check_modules(BMICXX REQUIRED IMPORTED_TARGET bmicxx)
message("--   bmicxx include - ${BMICXX_INCLUDE_DIRS}")
include_directories(${BMICXX_INCLUDE_DIRS})
pkg_check_modules(GRPC4BMI REQUIRED grpc4bmi heatcxx)

add_executable(run_bmi_server run_bmi_server.cc)

target_include_directories(run_bmi_server PRIVATE)

target_link_libraries(run_bmi_server
                      ${GRPC4BMI_LINK_LIBRARIES}
                      )

install(TARGETS run_bmi_server
        RUNTIME DESTINATION bin)
