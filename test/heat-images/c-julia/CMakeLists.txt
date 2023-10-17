cmake_minimum_required(VERSION 3.0)
project(run_bmi_server C CXX)

set(CMAKE_MACOSX_RPATH 1)
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

set(_cflags "-ansi -Wall -Wundef -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations -O2")
find_package(PkgConfig REQUIRED)
pkg_check_modules(BMIC REQUIRED IMPORTED_TARGET bmic)
message("--   bmic include - ${BMIC_INCLUDE_DIRS}")
include_directories(${BMIC_INCLUDE_DIRS})
pkg_check_modules(GRPC4BMI REQUIRED grpc4bmi)

# See https://github.com/barche/embedding-julia
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR})
find_package(Julia REQUIRED)

add_definitions(-DJULIA_ENABLE_THREADING)

add_executable(run_bmi_server run_bmi_server.cc)

target_include_directories(run_bmi_server PRIVATE "$<BUILD_INTERFACE:${Julia_INCLUDE_DIRS}>")

target_link_libraries(run_bmi_server
                      ${GRPC4BMI_LINK_LIBRARIES}
                      $<BUILD_INTERFACE:${Julia_LIBRARY}>
                      )

install(TARGETS run_bmi_server
        RUNTIME DESTINATION bin)
