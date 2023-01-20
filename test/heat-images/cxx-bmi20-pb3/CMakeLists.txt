cmake_minimum_required(VERSION 3.0)

find_package(protobuf REQUIRED)
find_package(grpc REQUIRED)
find_package(grpc++ REQUIRED)
find_package(grpc4bmi REQUIRED)
find_package(heatcxx REQUIRED)

add_executable(run_heat_bmi_model run_heat_bmi_model.cxx)
