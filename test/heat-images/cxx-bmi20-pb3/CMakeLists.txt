cmake_minimum_required(VERSION 3.0)
project(run_bmi_server)

find_package(PkgConfig REQUIRED)
pkg_check_modules(BMI REQUIRED bmic bmicxx)
pkg_check_modules(GRPC4BMI REQUIRED protobuf grpc++ grpc4bmi heatcxx)

add_executable(run_bmi_server run_bmi_server.cc)

target_include_directories(run_bmi_server PRIVATE)

target_link_libraries(run_bmi_server
                      ${GRPC4BMI_LINK_LIBRARIES}
                      )

install(TARGETS run_bmi_server
        RUNTIME DESTINATION bin)
